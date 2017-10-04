# -*- coding: utf-8 -*-
"""
Django settings for corretaza-buscador
"""
from __future__ import absolute_import, unicode_literals

import environ
from os.path import basename, dirname, join, normpath
from sys import path

from easy_thumbnails.conf import Settings as thumbnail_settings

# Load operating system environment variables
env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Absolute filesystem path to the Django project directory:
BASE_DIR = dirname(dirname(__file__))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(BASE_DIR)

SITE_NAME = basename(BASE_DIR)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(BASE_DIR)

ADMINS = (
    ('Roger', 'roger@na-inter.net'),
)

MANAGERS = ADMINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default=r"ll=&4)2zk&-2jy!o7j9#5dj+^b5=53vha1m-*o#x3rde%=@g=-")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_CORRETAZA_DEBUG', False)

TEMPLATE_DEBUG = DEBUG

THUMBNAIL_DEBUG = DEBUG

DEVELOPMENT = env.bool('DJANGO_CORRETAZA_DEVELOPMENT', False)

SEND_BROKEN_LINK_EMAILS = True

ALLOWED_HOSTS = []

ROOT_URLCONF = '%s.urls' % SITE_NAME

WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('SEUCORRETOR_DB_NAME', default='seucorretor'),
        'USER': env('SEUCORRETOR_DB_USER', default='seucorretor'),
        'PASSWORD': env('SEUCORRETOR_DB_PASSWORD', default=''),
        'HOST': env('SEUCORRETOR_DB_HOST', default='localhost'),
        'PORT': '3306',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB;SET foreign_key_checks=0;',
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))
MEDIA_URL = '/media/'

STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# django-bower (find the bower folder)
BOWER_COMPONENTS_ROOT = normpath(join(SITE_ROOT, 'components'))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)


FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'imobiliaria.context_processors.userprofile_processor',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
    normpath(join(SITE_ROOT, 'themes', 'templates')),       # django-floppyforms
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tracking.middleware.PageViewsMiddleware',
)

# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    #'django.contrib.sitemaps',       # App to generate the sitemaps
)

THIRD_PARTY_APPS = (
    #'south',                          # Database migration helpers
    'djangobower',                    # django-bower
    'floppyforms',                    # django-floppyforms
    'django_extensions',              # django-extensions
    'ckeditor',                       # django-ckeditor-updated
    'easy_thumbnails',                # django-image-cropping
    'image_cropping',                 # django-image-cropping
    'chartkick',
    'magicemailtemplates',
    'rolepermissions',
    'django_crontab',
)

LOCAL_APPS = (
    'core',
    'autoatendimento',
    'pcorretor',
    'pclientes',
    'themes',
    'signup',
    'atividades',
    'vivareal',
    'zapimoveis',
    'tracking',
    'relatorios',
    'cidades',
    'ibuscador',
    'crm',
    'imobiliaria',
    'imoveis',
    'buscacep',
    'parceiros',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# django-ckeditor-updated
CKEDITOR_UPLOAD_PATH = normpath(join(MEDIA_ROOT, 'uploads'))
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 340,
        'width': 680,
    },
}

######## REGISTRATION and LOGIN
#ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL = '/signup/auth/'
LOGIN_REDIRECT_URL = '/userpage/'
AUTH_PROFILE_MODULE = 'signup.UserProfile'
PASSWORD_MINIMUM_LENGHT = 6

# django-image-cropping
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

# ######### EMAIL CONFIGURATION
#Mailgun
SERVER_EMAIL = env('DJANGO_CORRETAZA_SERVER_EMAIL',
                   default='Corretaza Imoveis <contato@corretaza.com.br>')
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = env('DJANGO_CORRETAZA_MAILGUN_ACCESS_KEY', default='key-...')
MAILGUN_SERVER_NAME = env('DJANGO_CORRETAZA_MAILGUN_SERVER_NAME', default='corretaza.com.br')

# ######### PERMISSIONS
# rolepermissions
ROLEPERMISSIONS_MODULE = 'seucorretor.roles'
#ROLEPERMISSIONS_REDIRECT_TO_LOGIN = True

# django-crontab
CRONTAB_DJANGO_SETTINGS_MODULE = 'seucorretor.settings.production'
CRONJOBS = [
    ('0 6-22 * * *', 'django.core.management.call_command',
     ['importa_interesses_imovelweb'],
     {'file': 'autoatendimento/imovelweb.json'},
     '2>&1 > /tmp/django-crontab.log'),
]

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': [],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}
