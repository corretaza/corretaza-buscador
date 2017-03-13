# -*- coding: utf-8 -*-

from .base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

THUMBNAIL_DEBUG = DEBUG

DEVELOPMENT = True

ADMINS = (
    ('', ''),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# django-debug-toolbar
#INSTALLED_APPS += (
#    'debug_toolbar',
#)

#MIDDLEWARE_CLASSES += (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
#)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# ATENÇÃO: Dentro do Docker o IP não é este
INTERNAL_IPS = ('127.0.0.1', )

def show_toolbar_callback(request):
    """ Mostra a barra de debug para todos os requests NAO AJAX """
    return not request.is_ajax()

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'seucorretor.settings.development.show_toolbar_callback',
}

# # General settings
ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]
