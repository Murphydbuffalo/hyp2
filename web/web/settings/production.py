from .base import * # noqa F403
from .base import MIDDLEWARE, DATABASES, LOGGING
from os import environ

DEBUG = False

SECRET_KEY = environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    "app.onhyp.com",
]

INTERNAL_IPS = []

AIRBRAKE = dict(
    project_id=environ.get("AIRBRAKE_PROJECT_ID"),
    project_key=environ.get("AIRBRAKE_API_KEY"),
)

RQ_QUEUES = {
    'default': {
        'URL': environ.get('REDISTOGO_URL'),
        'DEFAULT_TIMEOUT': 900,
    },
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'hyp': {
            'handlers': ['console', 'airbrake'],
            'level': 'INFO',
            'propagate': True,
        },
        "rq.worker": {
            "handlers": ["rq_console"],
            "level": "INFO"
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'airbrake': {
            'level': 'ERROR',
            'class': 'pybrake.LoggingHandler',
        },
        "rq_console": {
            "level": "INFO",
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "rq_console",
            "exclude": ["%(asctime)s"],
        },
    },
    "formatters": {
        "rq_console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
}

MIDDLEWARE.append('pybrake.django.AirbrakeMiddleware')

EMAIL_HOST = 'smtp.postmarkapp.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = environ.get('POSTMARK_ACCESS_TOKEN')
EMAIL_HOST_PASSWORD = environ.get('POSTMARK_ACCESS_TOKEN')

DATABASES['default']['OPTIONS'] = {"sslmode": "require"}

# We manually run the `collectstatic` command in `bin/post_compile`, which is a
# script Heroku runs before deploying the app. This allows us to compile Sass to
# CSS prior to running `collectstatic`.
DISABLE_COLLECTSTATIC = 1
