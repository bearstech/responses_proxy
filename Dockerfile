FROM python:3-alpine

COPY . /responses_proxy

RUN cd /responses_proxy && pip install . && \
    rm -Rf /responses_proxy /root/.cache /.cache

VOLUME /tests/responses

ENTRYPOINT ["responses-proxy"]
