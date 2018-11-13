FROM python:3

LABEL author.blog="https://tyvik.ru"
LABEL author.email="tyvik8@gmail.com"
LABEL project.site="https://geopuzzle.org"
LABEL project.repo="https://github.com/TyVik/geopuzzle"

RUN apt-get update && \
    apt-get install -y \
        gdal-bin

COPY . /home/tyvik/geopuzzle/
RUN mv /home/tyvik/geopuzzle/.env_docker /home/tyvik/geopuzzle/.env
RUN mkdir /home/tyvik/logs
RUN mkdir /home/tyvik/geopuzzle/logs

WORKDIR /home/tyvik/geopuzzle
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["/home/tyvik/geopuzzle/entrypoint.sh"]