# -*- coding: utf-8 -*-
from .base import *

DEBUG = True

# UPDATE HERE: The below ALLOWED_HOSTS must contain the nginx server_url,
#              otherwise, you'll get a BAD REQUEST ERROR
ALLOWED_HOSTS = ['seucorretor.na-inter.net', '127.0.0.1', ]

# ######### EMAIL CONFIGURATION
# djrill
#MANDRILL_API_KEY = "RLMV5rUKNHd6tBTCknmVLA"  # roger@na-inter.net API Key
#EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
#SERVER_EMAIL = 'SJC Vale Imoveis <roger@na-inter.net>'
#DEFAULT_FROM_EMAIL = SERVER_EMAIL
#DJRILL_WEBHOOK_SECRET = "khq2OOyKSttlTtSx"

# Mailgun
#EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
#MAILGUN_ACCESS_KEY = 'key-c7b5d21b0609770dbfede4c9c2018dc5'
#MAILGUN_SERVER_NAME = 'na-inter.net'

# ######### EMAIL CONFIGURATION
# djrill
#MANDRILL_API_KEY = "a127t3ueNC77MBCPTU9k9Q"  # silvia@sjc API Key
#EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
SERVER_EMAIL = 'SJC Vale Imoveis <contato@sjcvaleimoveis.com.br>'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

#Mailgun
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-c7b5d21b0609770dbfede4c9c2018dc5'
MAILGUN_SERVER_NAME = 'sjcvaleimoveis.com.br'

# django-crontab
CRONTAB_DJANGO_SETTINGS_MODULE = 'seucorretor.settings.staging'
