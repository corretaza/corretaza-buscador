# -*- coding: utf-8 -*-
"""
Staging
"""

from .base import *  # noqa


DEBUG = True

# UPDATE HERE: The below ALLOWED_HOSTS must contain the nginx server_url,
#              otherwise, you'll get a BAD REQUEST ERROR
ALLOWED_HOSTS = env.list('DJANGO_CORRETAZA_ALLOWED_HOSTS',
                         default=['seucorretor.na-inter.net',
                                  '127.0.0.1', ])

# ######### EMAIL CONFIGURATION
SERVER_EMAIL = 'Corretaza Imoveis <contato@corretaza.com.br>'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

#Mailgun
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-...'
MAILGUN_SERVER_NAME = 'corretaza.com.br'

# django-crontab
CRONTAB_DJANGO_SETTINGS_MODULE = 'seucorretor.settings.staging'
