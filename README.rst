===================
responses proxy
===================

.. image:: https://travis-ci.org/bearstech/responses_proxy.png?branch=master
  :target: https://travis-ci.org/bearstech/responses_proxy

responses_proxy allow you to easily mock HTTP responses in your tests

Installation
=============

With pip::

    $ pip install responses_proxy

Using docker::

    $ docker run --rm -v tests/responses:/tests/responses bearstech/responses_proxy -h

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

NB: With docker you'll have to mount the volume::

    $ docker run --rm -v tests/responses:/tests/responses bearstech/responses_proxy

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
