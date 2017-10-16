FROM python:3-alpine

RUN pip install responses_proxy && rm -Rf /root/.cache

VOLUME /tests/responses

CMD ["responses-proxy"]
