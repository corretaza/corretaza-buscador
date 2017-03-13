from os import getenv, pardir
from os.path import abspath, basename, dirname, join, normpath, exists, isdir

from datetime import datetime
from optparse import make_option

from django.template import Context, Template
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import models


class Command(BaseCommand):
    help = "Create the nginx file"
    option_list = BaseCommand.option_list + (
        make_option('--env', action='store', dest='env', type="string", help='Set environment'),
        make_option('--url', action='store', dest='url', type="string", help='Set the server url'),
        make_option('--nginx', action='store', dest='nginx', type="string", help='Set the NGINX folder'),
    )    

    def handle(self, *args, **options):
        """ """
        BASE_DIR = settings.BASE_DIR
        SITE_ROOT = dirname(BASE_DIR)
        REPO_DIR = abspath(join(SITE_ROOT, pardir))
        PROJECT_NAME = basename(BASE_DIR)

        environment = options['env']
        server_url = options['url']
        NGINX_TARGET_FOLDER = options['nginx']

        DATA = dict(
                    environment = '%s' % environment,
                    project_name = '%s' % PROJECT_NAME,
                    server_url = '%s' % server_url,
                    project_repo_folder = REPO_DIR,
        )

        NGINX_CONF_SOURCE = "%s/nginx.%s" % (join(REPO_DIR, 'config/nginx'), environment) 
        NGINX_FILE = "%s/sites-available/%s_%s" % (NGINX_TARGET_FOLDER, PROJECT_NAME, environment)
    
        content = open(NGINX_CONF_SOURCE, 'r')
        template = Template(content.read())
        content.close()
        content = open(NGINX_FILE, 'w+')
        content.write(template.render(Context(DATA)))
        content.close()

        self.stdout.write('nginx file created successfuly\n')
