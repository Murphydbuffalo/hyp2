from .base import * # noqa F403
from os import environ

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '2b318f4d13897f'
EMAIL_HOST_PASSWORD = environ.get('MAILTRAP_PASSWORD')
EMAIL_PORT = '2525'
