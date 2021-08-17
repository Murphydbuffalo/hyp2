#!/bin/sh

set -e

cd web

python manage.py sass hyp/static/scss hyp/static/css -t compressed
python manage.py check --deploy --fail-level WARNING
python manage.py migrate
