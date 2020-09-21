#!/bin/sh

cd web
python manage.py check --deploy
python manage.py migrate
