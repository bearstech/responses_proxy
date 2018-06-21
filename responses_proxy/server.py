import os
import sys
import json
import argparse

import webob
import requests
import waitress
import urllib3

# ssl warnings are useless for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def default_from_env(key, default):
    value = os.getenv('RESPONSES_PROXY_' + key.replace('-', '_').upper())
    if not value:
        return default
    if isinstance(default, bool):
        return True
    elif isinstance(default, int):
        return int(value)
    elif isinstance(default, list):
        return value.split(',')
    return value


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--docroot', metavar='DIRNAME',
                        default=default_from_env('docroot', 'tests/responses'))
    parser.add_argument('--proxy', action='store_true',
                        default=default_from_env('proxy', False))
    parser.add_argument('--proxy-domain', action='append',
                        default=default_from_env('domains', []),
                        help='always proxy those hosts')
    parser.add_argument('--use-ssl', action='store_true',
                        default=default_from_env('use_ssl', False),
                        help='always convert http to https')
    parser.add_argument('--ssl-domain', action='append',
                        default=default_from_env('ssl_domains', []),
                        help='convert http to https for this host')
    parser.add_argument('--host', metavar='HOST',
                        default=default_from_env('host', '0.0.0.0'))
    parser.add_argument('--port', metavar='3333', type=int,
                        default=default_from_env('port', 3333))
    parser.add_argument('--debug', action='store_true',
                        default=default_from_env('debug', False))
    return parser.parse_args(args)


class MockServer:

    # thoses are not supported by the wsgi specs
    exclude_response_headers = [
        'Transfer-Encoding',
        'Content-Encoding',
        'Connection'
    ]

    exclude_request_headers = ['Host']

    def __init__(self, args):
        self.args = args

    def build_response(self, data, body):
        resp = webob.Response()
        resp.status_int = data['status']
        resp.headers.update({str(k): str(v) for k, v in data['headers']})
        resp.body = body
        if self.args.debug:
            print(resp)
            print('---\n\n')
        return resp

    def __call__(self, environ, start_response):
        req = webob.Request(environ)
        full_path = req.path_info
        if req.query_string:
            full_path += '?' + req.query_string
        filename = os.path.join(
            self.args.docroot,
            req.host,
            ''.join([c if c not in '[]{}()!?&-=,%' else '_'
                     for c in full_path[:250].lstrip('/')]),
            '__{}__'.format(req.method))
        scheme = 'https://' if self.args.use_ssl else 'http://'
        if req.host in self.args.ssl_domain:
            scheme = 'https://'
        url = scheme + req.host + full_path
        if self.args.debug:
            print(url)
            print('---')
            print(req)
            print('---')
        else:
            print("{0} {1}".format(req.method, url))
        if self.args.proxy or req.host in self.args.proxy_domain:
            resp = requests.request(
                req.method.upper(),
                url,
                data=req.body,
                headers={k: v for k, v in req.headers.items()
                         if k not in self.exclude_request_headers},
                allow_redirects=False,
                verify=False,
            )
            if self.args.debug:
                print(resp)
                print('---')

            data = {
                'url': url,
                'method': req.method.upper(),
                'status': resp.status_code,
                'headers': [(k, v.replace('https://', 'http://'))
                            for k, v in resp.headers.items()
                            if k not in self.exclude_response_headers],
            }
            if req.host in self.args.proxy_domain:
                resp = self.build_response(data, resp.content)
                sys.stdout.flush()
                return resp(environ, start_response)

            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(filename + '.json', 'w') as fd:
                json.dump(data, fd)
            with open(filename + '.body', 'wb') as fd:
                fd.write(resp.content)

        with open(filename + '.json') as fd:
            data = json.load(fd)

        with open(filename + '.body', 'rb') as fd:
            body = fd.read()

        resp = self.build_response(data, body)

        sys.stdout.flush()

        return resp(environ, start_response)


def main():
    args = parse_args()
    app = MockServer(args)
    print((
        'Starting server on http://{0.host}:{0.port} '
        'with options {0}'
        ).format(args))
    sys.stdout.flush()
    waitress.serve(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
