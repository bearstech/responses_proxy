FROM python:3

RUN pip install responses_proxy

VOLUME /tests/responses

CMD ["responses-proxy"]
