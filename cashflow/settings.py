"""
Django settings for cashflow project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os  # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import raven
import re
import dj_database_url
from django.conf.global_settings import AUTHENTICATION_BACKENDS, SESSION_COOKIE_AGE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = BASE_DIR

# noinspection PyRedeclaration
AUTHENTICATION_BACKENDS = ['cashflow.dauth.DAuth']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '-01^^veefr*f_p=phew0w7ib37_738%=lwmp9n4bl_2*5^)vjy')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', 'False') == "True")
print(DEBUG)

GOOGLE_ANALYTICS_KEY = os.getenv('GOOGLE_ANALYTICS_KEY')

ALLOWED_HOSTS = ['*']

# CORS configuration
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'raven.contrib.django.raven_compat',
    'storages',
    'corsheaders',
    'widget_tweaks',
    'expenses',
    'invoices',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'cashflow.dauth.AuthRequiredMiddleware',
)

ROOT_URLCONF = 'cashflow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'string_if_invalid': '%s',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Raven/sentry config
if not DEBUG:
    RAVEN_CONFIG = {
        'dsn': 'https://8454517d78524997a90a51fdab243d7b:8bddac8028dd41daa99198c80c80ba2a@sentry.io/1256268',
        # Configure release based on git hash
        'release': os.getenv('GIT_REV'),
    }


WSGI_APPLICATION = 'cashflow.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
if os.environ.get("DATABASE_URL"):  # Stuff for when running in Dokku.

    # Parse the DATABASE_URL env var.
    # First group is the (ql)? group, hence _
    _, USER, PASSWORD, HOST, PORT, NAME = re.match(
        "^postgres(ql)?://(?P<username>.*?):(?P<password>.*?)@(?P<host>.*?):(?P<port>\d+)/(?P<db>.*?)$",
        os.environ.get("DATABASE_URL", "")).groups()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': NAME,
            'USER': USER,
            'PASSWORD': PASSWORD,
            'HOST': HOST,
            'PORT': PORT,
        }
    }
else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'cashflow'),
            'USER': os.getenv('DB_USER', 'cashflow'),
            'PASSWORD': os.getenv('DB_PASS', 'cashflow'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# noinspection PyRedeclaration
SESSION_COOKIE_AGE = 60 * 60 * 24 * 2  # Sessions expire after 2 days

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'sv-SE'

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_API_KEY = os.getenv('LOGIN_KEY', 'key-012345678910111213141516171819')
AUTH_URL = os.getenv('LOGIN_URL', 'https://login.datasektionen.se')

SEND_EMAILS = (os.getenv('SEND_EMAILS', False) == 'True')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'staticfiles'),)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'se.datasektionen.foo')
AWS_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', 'xxxxxxxxxxxxxxxxxxxx')
AWS_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

AWS_S3_HOST = os.getenv('S3_HOST', 's3.eu-central-1.amazonaws.com')
AWS_S3_CUSTOM_DOMAIN = "{0}.s3.amazonaws.com".format(AWS_STORAGE_BUCKET_NAME)

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://{0}/{1}/".format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'expenses.custom_storages.MediaStorage'

SPAM_API_KEY = os.getenv('SPAM_API_KEY', 'Lobster Thermidor au Crevette with a Mornay sauce garnished with truffle '
                                         'pate, brandy and with a fried egg on top and spam.')
SPAM_URL = os.getenv('SPAM_URL', 'https://spam.datasektionen.se')

PLS_URL = os.getenv('PLS_URL', 'https://pls.datasektionen.se')
