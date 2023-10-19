[![CircleCI](https://circleci.com/gh/TyVik/geopuzzle.svg?style=svg)](https://circleci.com/gh/TyVik/geopuzzle)
[![BrowserStack Status](https://www.browserstack.com/automate/badge.svg?badge_key=Fbm86tXoBBqACUnFaJqP)](https://www.browserstack.com/automate/public-build/Fbm86tXoBBqACUnFaJqP)
[![codecov](https://codecov.io/gh/TyVik/geopuzzle/branch/develop/graph/badge.svg)](https://codecov.io/gh/TyVik/geopuzzle)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=TyVik_geopuzzle&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=TyVik_geopuzzle)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=TyVik_geopuzzle&metric=alert_status)](https://sonarcloud.io/dashboard?id=TyVik_geopuzzle)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=TyVik_geopuzzle&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=TyVik_geopuzzle)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=TyVik_geopuzzle&metric=security_rating)](https://sonarcloud.io/dashboard?id=TyVik_geopuzzle)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=TyVik_geopuzzle&metric=sqale_index)](https://sonarcloud.io/dashboard?id=TyVik_geopuzzle)

# Intro

![geopuzzle](https://github.com/TyVik/geopuzzle/raw/1e8c970da66e35d8e11f9805355c7d041c7ebc95/static/images/puzzle.gif) 
Arrange the pieces of the world! You need to drag the shape of the territory to the right place. 
Just like in childhood we collected pictures piece by piece, so here you can collect a country 
from regions or whole continents from countries! 

Furthermore second variation is the Quiz. In the Quiz you need find the country by flag, emblem 
or the capital. 

# Installation

This is just web application, so you need:

1. nginx (as balancer)
2. wsgi (gunicorn, for example)
3. asgi (daphne, for example)
4. supervisor (or run apps in docker compose)
5. python >= 3.11 (with pdm)
6. redis >= 5.0
7. postgres >= 12
8. nodejs >= 20.8

## Postgres

This extensions must be installed:

- postgis
- postgis_topology
- postgis_sfcgal
- fuzzystrmatch
- address_standardizer
- postgis_tiger_geocoder

For example:

```postgresql
create user geopuzzle with password 'geopuzzle';
create database geopuzzle owner geopuzzle;
create extension postgis;
```

## Nodejs

Necessary for build frontend. npm commands:

- `test` - run test locally
- `testci` - run test on CI/CD
- `analyze` - analyze build
- `dev` - run dev server
- `build` - build static for production

## python && pdm

I use pdm for manage dependencies and run commands. Install [pdm-django](https://pypi.org/project/pdm-django/) plugin via `pdm plugin add pdm-django`. 
Run management commands like `pdm manage runserver` - to run dev server.

### Special management commands

- `cache` - update/import/export and recalculate polygon cache (from postgres to redis)
- `clearcache` - clear django decorators cache
- `deploystatic` - upload static to S3
- `fix_infobox_links` - update wiki if any link is not valid
- `update_geometry` - update polygon and wiki data from external source (OSM and Wikidata)
- `validate_infoboxes` - check that all required data in all infoboxes is filled and correct

## nginx

Nginx requires for traffic balancer:

- `/` to wsgi app
- `/ws` to asgi app

Example configuration is placed in `deploy` directory.

## wsgi / asgi

Games work via websockets, so you have to run both wsgi and asgi server for production:

- wsgi - `gunicorn mercator.wsgi:application -b 0.0.0.0:8000`
- asgi - `daphne mercator.asgi:application -b 0.0.0.0 -p 8001`

`./manage.py runserver` starts both of them at the same time. This project is a django application so envs are common.

### Environment variables

All envs are placed in `.env_template` file. Most of them have a default value, so you can copy `.env_template` to `.env` for the first run.

Describe some special variables:

- `OSM_KEY` - load polygons from OpenStreetMap
- `GOOGLE_KEY` - production key for Google Maps API (not required)
- `DISABLE_GOOGLE_KEY` - temporary disable `GOOGLE_KEY` (empty or "True")
- `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` - AWS uses to deploy static and CDN
- `SOCIAL_VK_KEY`/`SOCIAL_VK_SECRET` - enable VK authorization
- `SOCIAL_FACEBOOK_KEY`/`SOCIAL_FACEBOOK_SECRET` - enable Facebook authorization
- `SOCIAL_GOOGLE_KEY`/`SOCIAL_GOOGLE_SECRET` - enable Google authorization

### Load data

I find excellent service for load geojson files with polygons - https://osm-boundaries.com/.
Just select the country (or many or with regions) and click 'Export'. URL must be like:
```
https://osm-boundaries.com/Download/Submit?apiKey=74ba654a378b8daf80f&db=osm20210531&osmIds=-5682946,-5682950&format=GeoJSON&srid=4326
```
And download content by that link. You've got zip archive with GeoJson files, unpack them into `geojson` folder.
After that you can run management command `(venv)$ ./manage.py update_regions` for load polygons into database.
Take into account - data from OSM is not perfect and some regions can have bad or recursive links to each other.
In most cases, restarting can help :) 

You can download [sample database](https://drive.google.com/open?id=1H_JUXr39Q-W2_153qHgbQD80FOUSU-JM).
Unpack archive into `pgdata` directory.

## Docker images

Project has 2 Dockerfiles:

* /Dockerfile.backend - for server side (django tests and deploy)
* /Dockerfile.frontend - for client side (webpack build bundles and jest tests)

All images should be up to date with all installed dependencies. This allows you to significantly reduce the time to perform tasks CI.
Command for update image (backend, by example):

```bash
$ docker build --build-arg GIT_REVISION=$(git rev-parse --short HEAD) -t tyvik/geopuzzle:backend --target backend -f Dockerfile.backend .
```

# Useful links

* https://osm-boundaries.com/
* http://global.mapit.mysociety.org/areas/O03 - http://mapit.poplus.org/docs/self-hosted/how-data-is-stored/
* http://geo.koltyrin.ru/
* http://www.marineregions.org/gazetteer.php?p=browser&id=1900&expand=true#ct

# Useful services

[<img src="https://cloud.githubusercontent.com/assets/7864462/12837037/452a17c6-cb73-11e5-9f39-fc96893bc9bf.png" alt="Browser Stack Logo" width="400">](https://www.browserstack.com/)