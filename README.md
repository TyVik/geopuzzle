# Intro

![geopuzzle](https://raw.githubusercontent.com/TyVik/geopuzzle/master/static/images/puzzle.png) 
Arrange the pieces of the world! You need to drag the shape of the territory to the right place. 
Just like in childhood we collected pictures piece by piece, so here you can collect a country 
from regions or whole continents from countries! 

Furthermore second variation is the Quiz. In the Quiz you need find the country by flag, emblem 
or the capital. 

# Installation

This is just web application, so you need:

1. nginx 
2. uwsgi
3. supervisor
4. python >= 3.5
5. redis
6. postgres >= 9.5
7. nodejs 6.x

## System applications

Install nginx, uwsgi, supervisor and other packages:
```
$ sudo apt install nginx uwsgi uwsgi-plugin-python3 supervisor redis
$ sudo apt install gdal-bin gettext build-essential python3-dev libpq-dev
```

Template config files for nginx, uwsgi and supervisor are placed in `deploy` directory.
I hope python 3 with pip already installed :)

## Create virtual environment

```
$ virtualenv --python=`which python3` geopuzzle
```

## Create database

1. Install Postgres with PostGIS:
    ```
    $ sudo apt install postgresql postgresql-contrib postgis
    ```

2. Install postgis extension:
    ```
    $ sudo su postgres -c psql
    postgres=# create user geopuzzle with password "geopuzzle";
    postgres=# create database geopuzzle owner geopuzzle;
    ``` 
3. Create user and database:
    ```
    $ sudo su postgres -c psql
    postgres=# \c geopuzzle
    geopuzzle=# create extension postgis;
    geopuzzle=# create extension postgis_topology;
    geopuzzle=# create extension postgis_sfcgal;
    geopuzzle=# create extension fuzzystrmatch;
    geopuzzle=# create extension address_standardizer;
    geopuzzle=# create extension postgis_tiger_geocoder;
    ```
4. Create tables:
    ```
    (geopuzzle)$ ./manage.py migrate
    ```

## Set up env variables

All environment variables are collected in .env file (.env_template is template for that). 
Some variables such as REDIS_HOST or DJANGO_SETTINGS_MODULE do not require explanation. 
But some are specific to the project:

* OSM_KEY need only for load polygons into database
* GOOGLE_KEY is production key for Google Maps API (preferred, but not required)
* RAVEN_DSN for collect errors to Sentry (optional)

* AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY need only for AWS settings usage. Can left them blank.


## Build static files

Install nodejs:
```
$ sudo apt install nodejs npm
$ npm init
$ npm run build
(geopuzzle)$ ./manage.py collectstatic
```

# Load data

I find excellent service for load geojson files with polygons - https://wambachers-osm.website/boundaries/.
Just select the country (or many or with regions) and click 'Export'. URL must be like:
```
https://wambachers-osm.website/boundaries/exportBoundaries?apiversion=1.0&apikey=434e16bd-cdd3-489f-ab39-d0ee2e6f894f&exportFormat=json&exportLayout=levels&exportAreas=land&from_al=2&to_al=4&union=false&selected=16239
```
And download content by that link. You've got zip archive with GeoJson files, unpack them into `geojson` folder.
After that you can run management command `(geopuzzle)$ ./manage.py update_regions` for load polygons into database.
Take into account - data from OSM is not perfect and some regions can have bad or recursive links to each other.
In most cases, restarting can help :) 

# Management commands

Management command usually run via manage.py script, for example: `./manage.py import_region`.

* `cache` - import/export and recalculate cache (from postgres)
* `import_region` - load one .geojson into database
* `update_infobox` - update infobox from WikiData
* `update_regions` - load all .geojson into database from `geojson` folder
* `validate_infoboxes` - check that all required data in all infoboxes is filled and correct

# Useful links

* https://wambachers-osm.website/boundaries/
* http://global.mapit.mysociety.org/areas/O03 - http://mapit.poplus.org/docs/self-hosted/how-data-is-stored/
* http://geo.koltyrin.ru/
* http://www.marineregions.org/gazetteer.php?p=browser&id=1900&expand=true#ct
