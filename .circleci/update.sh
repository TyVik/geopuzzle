#!/bin/bash

source /home/tyvik/venv/bin/activate
git pull
pipenv install
python manage.py clearcache
python manage.py compilemessages
python manage.py migrate
touch reload
