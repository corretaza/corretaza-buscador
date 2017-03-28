"""
   Make the tests run faster on localmachines

   IMPORTANT: Avoid using this settins on staging and CI environments
"""
from .base import *

ADMINS = (
    ('', ''),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'dbtest.sqlite3'),
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]
