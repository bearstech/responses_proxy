import responses_proxy
import requests


def test_mock():
    with responses_proxy.RequestsMock():
        resp = requests.get('http://bearstech.com')
        assert resp.status_code == 200
