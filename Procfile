web: cd web && gunicorn web.wsgi
worker: cd web && python manage.py rqworker default

release: ./heroku.sh
