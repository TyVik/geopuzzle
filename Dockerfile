FROM tyvik/geopuzzle:app

RUN apk update --no-cache && \
    apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    gdal gdal-dev

COPY . /home/tyvik/geopuzzle/
WORKDIR /home/tyvik/geopuzzle

RUN mv /home/tyvik/geopuzzle/.env_template /home/tyvik/geopuzzle/.env && \
    mkdir /home/tyvik/logs && \
    mkdir /home/tyvik/geopuzzle/logs

EXPOSE 8000
CMD ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000