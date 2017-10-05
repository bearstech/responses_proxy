from responses_proxy import RequestsMock
import requests


def test_mock():
    with RequestsMock(document_root='tests/document_root'):
        resp = requests.get('http://bearstech.com')
        assert resp.status_code == 200
