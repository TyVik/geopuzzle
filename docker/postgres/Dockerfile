FROM postgres:9.6

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgis \
        postgresql-9.6-postgis-2.3 \
        postgresql-9.6-postgis-2.3-scripts && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./init-db.sh /docker-entrypoint-initdb.d/init-db.sh