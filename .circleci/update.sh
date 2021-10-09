#!/bin/bash

source /home/tyvik/venv/bin/activate
git pull
echo "GIT_REVISION=$(git rev-parse HEAD)" >> .env
poetry install --no-dev --no-root
python manage.py clearcache
python manage.py compilemessages
python manage.py migrate
sudo supervisorctl restart all
