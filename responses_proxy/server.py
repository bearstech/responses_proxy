import os
import json
import argparse

import webob
import requests
import waitress


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--docroot', metavar='DIRNAME',
                        default='tests/responses')
    parser.add_argument('--proxy', action='store_true', default=False)
    parser.add_argument('--use-ssl', action='store_true', default=False)
    parser.add_argument('--host', metavar='HOST', default='localhost')
    parser.add_argument('--port', metavar='3333', type=int, default=3333)
    parser.add_argument('--debug', action='store_true', default=False)
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

    def __call__(self, environ, start_response):
        req = webob.Request(environ)
        full_path = req.path_info
        if req.query_string:
            full_path += '?' + req.query_string
        filename = os.path.join(
            self.args.docroot,
            req.host,
            ''.join([c if c not in '?&-=,' else '_'
                    for c in full_path.lstrip('/')]),
            '__{}__'.format(req.method))
        scheme = 'https://' if self.args.use_ssl else 'http://'
        url = scheme + req.host + full_path
        if self.args.debug:
            print(url)
            print('---')
            print(req)
            print('---')
        if self.args.proxy:
            resp = requests.request(
                req.method.upper(),
                url,
                data=req.body,
                headers={k: v for k, v in req.headers.items()
                         if k not in self.exclude_request_headers},
                allow_redirects=False,
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
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(filename + '.json', 'w') as fd:
                json.dump(data, fd)
            with open(filename + '.body', 'wb') as fd:
                fd.write(resp.content)

        with open(filename + '.json') as fd:
            data = json.load(fd)
        resp = webob.Response()
        resp.status_int = data['status']
        resp.headers.update({str(k): str(v) for k, v in data['headers']})

        with open(filename + '.body', 'rb') as fd:
            resp.body = fd.read()

        if self.args.debug:
            print(resp)
            print('---\n\n')
        return resp(environ, start_response)


def main():
    args = parse_args()
    app = MockServer(args)
    waitress.serve(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
