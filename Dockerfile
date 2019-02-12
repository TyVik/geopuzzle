FROM tyvik/geopuzzle:app

RUN mkdir /app && mkdir /app/logs
WORKDIR /app

EXPOSE 8000
CMD ["python3"]