#!/bin/sh

set -e

cd web
python manage.py check --deploy --fail-level WARNING
python manage.py migrate
