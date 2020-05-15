"""
Django settings for flixfinder project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# noinspection PyUnresolvedReferences
from . import monkey_patch

import os
import os.path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'test')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'FALSE') == 'TRUE'

ALLOWED_HOSTS = [
    '*'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'corsheaders',
    'rest_framework',
    'ff_api',
    'ff_spa',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flixfinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, os.path.join('flixfinder', 'templates')),
            os.path.join(BASE_DIR, os.path.join('ff_spa', 'templates')),
            os.path.join(BASE_DIR, os.path.join('ff_api', 'templates')),
        ],
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

WSGI_APPLICATION = 'flixfinder.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Install PyMySQL as mysqlclient/MySQLdb to use Django's mysqlclient adapter
# See https://docs.djangoproject.com/en/2.1/ref/databases/#mysql-db-api-drivers
# for more information
import pymysql

pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()

if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.getenv('SQL_HOST', '/cloudsql/flixfinder-develop'),
            'USER': os.getenv('SQL_USER', 'django'),
            'PASSWORD': os.getenv('SQL_PASS', 'django'),
            'NAME': os.getenv('SQL_NAME', 'django'),
        }
    }
elif os.getenv('SQL_PROXY', None):
    # Alternatively we can use the Cloud SQL via the proxy.
    # To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.getenv('SQL_HOST', '127.0.0.1'),
            'PORT': os.getenv('SQL_PORT', '3306'),
            'USER': os.getenv('SQL_USER', 'django'),
            'PASSWORD': os.getenv('SQL_PASS', 'django'),
            'NAME': os.getenv('SQL_NAME', 'django'),
        }
    }

else:
    # Running locally so use the sqlie3 backend for development and testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = './static/static/'
SPA_ROOT = './static/'

FIREBASE_KEY_FILE = os.getenv(
    'FIREBASE_KEY_FILE',
    os.path.join(BASE_DIR, 'firebase_sa_key.json')
)
if not os.path.isfile(FIREBASE_KEY_FILE):
    FIREBASE_KEY_FILE = None

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'ff_api.authentication.FirebaseAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_CREDENTIALS = False

TD_API_HOST = 'tastedive.com'
TD_API_KEY = '369882-FlixFind-5MBQ0Q28'

MDB_API_HOST = "api.themoviedb.org"
MDB_API_KEY = "15d2ea6d0dc1d476efbca3eba2b9bbfb"

RAPID_API_HOST = "imdb8.p.rapidapi.com"
# RAPID_API_KEY = "f122227b79msh5596f9f95684992p1eadd8jsn453f2f9af865" # Brian Key
RAPID_API_KEY = "570c97ce3amsh4a783754d23bab6p1210f4jsn974b3d3ad149"  # Dan Key
