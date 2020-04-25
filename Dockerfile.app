FROM python:3.8-slim-buster

RUN mkdir /app && mkdir /app/logs
WORKDIR /app

RUN apt update \
  && apt install -y --no-install-recommends build-essential make gcc gdal-bin wget git \
  && wget -q https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && rm dockerize-linux-amd64-v0.6.1.tar.gz \
  && apt-get autoremove -y \
  && apt-get clean

RUN wget -q https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py && POETRY_HOME=/opt/poetry python get-poetry.py && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-dev --no-root

CMD ["python3"]
