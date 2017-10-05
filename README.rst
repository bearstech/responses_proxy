===================
responses proxy
===================

First save some stuff using the proxy mode::

    $ responses-proxy --proxy

If your target site use ssl then use::

    $ responses-proxy --proxy --use-ssl

The proxy do not support ssl so you need to make http request. But first set
the `HTTP_PROXY` env var::

    $ export HTTP_PROXY=http://localhost:3333

Then run some code to make some requests::

    python -c "import requests; requests.get('http://bearstech.com')"

This will generate some file in `document_root/`

You can now restart the server without the proxy mode and the client will react
the same way without calling the real server.

You can aslo use a `RequestsMock` in you unit tests::

    from responses_proxy import RequestsMock
    import requsests

    def test_url():
        with RequestsMock(document_root='/path/to/document_root'):
            requests.get('http://bearstech.com')
            # https will work to
            requests.get('https://bearstech.com')
