from os import pardir, symlink
from os.path import abspath, basename, dirname, join, normpath, lexists

from optparse import make_option

from django.template import Context, Template
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import models


class Command(BaseCommand):
    help = "Create the nginx file"
    option_list = BaseCommand.option_list + (
        make_option('--env', action='store', dest='env', type="string", help='Set environment'),
        make_option('--nginx', action='store', dest='nginx', type="string", help='Set the NGINX folder'),
    )    

    def handle(self, *args, **options):
        """ """
        BASE_DIR = settings.BASE_DIR
        SITE_ROOT = dirname(BASE_DIR)
        REPO_DIR = abspath(join(SITE_ROOT, pardir))
        PROJECT_NAME = basename(BASE_DIR)

        environment = options['env']
        NGINX_TARGET_FOLDER = options['nginx']

        NGINX_AVAILABLE = "%s/sites-available/%s_%s" % (NGINX_TARGET_FOLDER, PROJECT_NAME, environment)
        NGINX_ENABLED = "%s/sites-enabled/%s_%s" % (NGINX_TARGET_FOLDER, PROJECT_NAME, environment)
        
        if not lexists(NGINX_ENABLED):
            symlink(NGINX_AVAILABLE, NGINX_ENABLED)

        self.stdout.write('nginx sites-enabled successfuly\n')
