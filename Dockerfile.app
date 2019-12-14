FROM python:3.8-slim

RUN mkdir /app && mkdir /app/logs
WORKDIR /app

COPY Pipfile* /app/

RUN apt update \
  && apt install -y build-essential make gcc python3-gdal libgeos-dev wget git \
  && pip3 install pipenv \
  && pipenv install --dev --system \
  && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && rm dockerize-linux-amd64-v0.6.1.tar.gz \
  && rm -r /root/.cache/pip \
  && rm -r /root/.cache/pipenv \
  && apt-get remove -y --purge libgdal-dev make gcc build-essential wget \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

CMD ["python3"]
