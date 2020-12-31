"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from os import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY', '_5@i3yzg%99ootbe@r7w8z-o_0pa(1d*ukphx&5pogw27_)ba(')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get('DEBUG', 'ON') == 'ON'

AIRBRAKE = dict(
    project_id=environ.get("AIRBRAKE_PROJECT_ID", ""),
    project_key=environ.get("AIRBRAKE_API_KEY", ""),
)

if DEBUG is False:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'airbrake': {
                'level': 'ERROR',
                'class': 'pybrake.LoggingHandler',
            },
        },
        'loggers': {
            'app': {
                'handlers': ['airbrake'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }

ALLOWED_HOSTS = [
    "onhyp.com",
    "localhost",
    "127.0.0.1",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'hyp.apps.HypConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

if DEBUG is True:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG is True:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
else:
    MIDDLEWARE.append('pybrake.django.AirbrakeMiddleware')

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': environ.get('DB_HOST', ''),
        'PORT': environ.get('DB_PORT', ''),
        'USER': environ.get('DB_USER', ''),
        'PASSWORD': environ.get('DB_PASSWORD', ''),
        'NAME': environ.get('DB_NAME', 'hyp2'),
    }
}

if DEBUG is False:
    DATABASES['default']['OPTIONS'] = {"sslmode": "require"}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = Path(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'

LOGOUT_REDIRECT_URL = "/"
