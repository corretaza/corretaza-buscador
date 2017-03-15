# -*- coding: utf-8 -*-
from .base import *

DEBUG = True

# UPDATE HERE: The below ALLOWED_HOSTS must contain the nginx server_url,
#              otherwise, you'll get a BAD REQUEST ERROR
ALLOWED_HOSTS = ['seucorretor.na-inter.net', '127.0.0.1', ]

# ######### EMAIL CONFIGURATION
SERVER_EMAIL = 'SJC Vale Imoveis <contato@sjcvaleimoveis.com.br>'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

#Mailgun
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-c7b5d21b0609770dbfede4c9c2018dc5'
MAILGUN_SERVER_NAME = 'sjcvaleimoveis.com.br'

# django-crontab
CRONTAB_DJANGO_SETTINGS_MODULE = 'seucorretor.settings.staging'
