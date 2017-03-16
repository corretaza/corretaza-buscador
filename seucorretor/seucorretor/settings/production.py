# -*- coding: utf-8 -*-
"""
Production
"""

from .base import *  # noqa

## UPDATE HERE: The below ALLOWED_HOSTS must contain the nginx server_url,
##              otherwise, you'll get a BAD REQUEST ERROR
ALLOWED_HOSTS = env.list('DJANGO_CORRETAZA_ALLOWED_HOSTS',
                         default=['corretaza.com.br',
                                  'www.corretaza.com.br',
                                  '127.0.0.1', ])
