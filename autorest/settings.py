"""
This module is designed to do 2 things:

 1. Provide an interface (``get_setting``) for getting settings from
    ``django.conf.settings`` with settings in this file being the fallback
    default.
 2. Provide enough settings for this app to run as a standalone project.
"""

from django.conf import settings
import os
import sys


me = sys.modules[__name__]


def get_setting(name):
    """
    Hook for getting Django settings and using properties of this file as the
    default.
    """
    try:
        return getattr(settings, name, getattr(me, name, None))
    except NameError:
        pass
    return None


# setting `base_dir` before defaults since it needs to be used by `DATABASES`.
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# app settings
AUTOREST_ADMIN_SITE = 'django.contrib.admin.site'
AUTOREST_DEFAULT_USE_ADMIN_SITE = False
AUTOREST_DEFAULT_ENABLE = True
AUTOREST_CONFIG = {
    'auth': {
        'User': {
            'use_admin_site': True,
        },
    },
}


# standalone settings
BASE_DIR = base_dir
SECRET_KEY = 'not-a-very-good-secret'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'autorest',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'autorest.middleware.TimeDelayMiddleware',
]
ROOT_URLCONF = 'autorest.urls'
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
WSGI_APPLICATION = 'autorest.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(base_dir, 'db.sqlite3'),
    }
}
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
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'autorest.permissions.CustomModelPermissions',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
APPEND_SLASH = True

# local development settings
try:
    from .local_settings import *
except ImportError:
    pass
