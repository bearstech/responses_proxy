FROM python:3-alpine

RUN pip install responses_proxy==0.1.2 && rm -Rf /root/.cache

VOLUME /tests/responses

CMD ["responses-proxy", "--host", "0.0.0.0"]
