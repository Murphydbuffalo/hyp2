web: cd web && gunicorn web.wsgi
worker: cd web && python manage.py rqworker default
scheduler: cd web && python manage.py scheduler

release: ./heroku.sh
