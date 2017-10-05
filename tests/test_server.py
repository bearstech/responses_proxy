import os
import sys
import time
import pytest
import requests
import subprocess


@pytest.fixture(scope='function')
def proxy(request):
    p = subprocess.Popen([
        sys.executable, '-m', 'responses_proxy.server',
        '--proxy', '--use-ssl',
        '--docroot', 'tests/responses',
    ], stdout=sys.stdout, stderr=sys.stderr)
    os.environ['HTTP_PROXY'] = 'http://localhost:3333'
    # wait for server to start
    time.sleep(1)
    yield p
    del os.environ['HTTP_PROXY']
    p.kill()


@pytest.fixture(scope='function')
def server(request):
    p = subprocess.Popen([
        sys.executable, '-m', 'responses_proxy.server',
        '--docroot', 'tests/responses',
    ], stdout=sys.stdout, stderr=sys.stderr)
    os.environ['HTTP_PROXY'] = 'http://localhost:3333'
    # wait for server to start
    time.sleep(1)
    yield p
    del os.environ['HTTP_PROXY']
    p.kill()


def test_request_proxy(proxy):
    resp = requests.get('http://bearstech.com/')
    assert resp.status_code == 200


def test_request_server(server):
    resp = requests.get('http://bearstech.com/')
    assert resp.status_code == 200
