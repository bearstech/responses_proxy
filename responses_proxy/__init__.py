import os
import json
import responses


class EmptyMock:
    def __enter__(*args):
        pass

    def __exit__(*args):
        pass


class RequestsMock(responses.RequestsMock):

    def __init__(self, document_root='tests/responses'):
        super(RequestsMock, self).__init__(assert_all_requests_are_fired=False)
        for root, dirnames, filenames in os.walk(document_root):
            for filename in filenames:
                if filename.endswith('.json'):
                    path = os.path.join(root, filename)
                    with open(os.path.join(root, filename)) as fd:
                        data = json.load(fd)
                    with open(path[:-5] + '.body', 'rb') as fd:
                        body = fd.read()
                    url = data['url'].split('://', 1)[1]
                    for scheme in ('http://', 'https://'):
                        self.add(
                            responses.Response(
                                method=data['method'],
                                url=scheme + url,
                                status=data['status'],
                                headers=data['headers'],
                                body=body,
                                match_querystring=True,
                             ))


if 'HTTP_PROXY' in os.environ:
    # if we use a proxy, forwards all query to it. do not use responses
    class RequestsMock(EmptyMock):  # NOQA
        pass
