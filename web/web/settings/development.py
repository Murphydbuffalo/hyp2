from .base import * # noqa F403
from .base import MIDDLEWARE, INSTALLED_APPS

from os import environ

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS.append('debug_toolbar')
INSTALLED_APPS.append('django_sass')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '2b318f4d13897f'
EMAIL_HOST_PASSWORD = environ.get('MAILTRAP_PASSWORD')
EMAIL_PORT = '2525'
