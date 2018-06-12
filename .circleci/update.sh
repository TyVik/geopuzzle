#!/bin/bash

git pull
pip install -r requirements.txt
python manage.py compilemessages
python manage.py migrate
touch reload