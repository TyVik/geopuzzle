FROM python:3.6-alpine3.7

RUN mkdir /app && mkdir /app/logs
WORKDIR /app

COPY Pipfile* /app/

RUN apk update --no-cache \
  && apk add --no-cache git openssh-client \
  && apk add --no-cache --virtual .postgres-deps py3-psycopg2 postgresql-libs postgresql-dev \
  && apk add --no-cache --virtual .build-deps libffi-dev build-base zlib-dev jpeg-dev gcc \
  && apk add --upgrade --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main libressl2.7-libcrypto \
  && apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main libressl2.7-libcrypto libcrypto1.1 \
  && apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing geos gdal \
  && pip3 install pipenv \
  && pipenv install --dev --system \
  && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && rm dockerize-linux-amd64-v0.6.1.tar.gz \
  && apk del .build-deps && apk del .postgres-deps

CMD ["python3"]
