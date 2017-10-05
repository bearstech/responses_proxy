===================
responses proxy
===================

responses_proxy allow you to easily mock HTTP responses in your tests

Installation
=============

::

    $ pip install responses_proxy

Usage
=====

Check command line arguments::

    $ responses-proxy -h

First save some stuff using the proxy mode::

    $ responses-proxy --proxy

If your target site use ssl then use::

    $ responses-proxy --proxy --use-ssl

The proxy do not support ssl so you need to make http request. But first set
the `HTTP_PROXY` env var::

    $ export HTTP_PROXY=http://localhost:3333

Then run some code to make some requests::

    python -c "import requests; requests.get('http://bearstech.com')"

This will generate some file in `tests/responses/`

You can now restart the server without the proxy mode and the client will react
the same way without calling the real server.

You can aslo use a `RequestsMock` in you unit tests::

    import responses_proxy
    import requsests

    def test_url():
        with responses_proxy.RequestsMock():
            requests.get('http://bearstech.com')
            # https will work to. both are registered
            requests.get('https://bearstech.com')
