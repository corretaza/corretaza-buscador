from os import getenv, pardir, symlink
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
        make_option('--user', action='store', dest='user', type="string", help='Set the unix user to run gunicorn'),
    )    

    def handle(self, *args, **options):
        """ """
        BASE_DIR = settings.BASE_DIR
        SITE_ROOT = dirname(BASE_DIR)
        REPO_DIR = abspath(join(SITE_ROOT, pardir))
        VIRTUALENV_DIR = abspath(join(REPO_DIR, pardir))
        PROJECT_NAME = basename(BASE_DIR)

        environment = options['env']
        user = options['user']

        DATA = dict(
                    environment = '%s' % environment,
                    project_name = '%s' % PROJECT_NAME,
                    user = '%s' % user,
                    project_base_folder = SITE_ROOT,
                    virtualenv_folder = VIRTUALENV_DIR,
        )

        GUNICORN_CONF_SOURCE = "%s/gunicorn.%s" % (join(REPO_DIR, 'config/nginx'), environment) 
        GUNICORN_FILE = "/etc/init/gunicorn-%s_%s.conf" % (PROJECT_NAME, environment)
    
        content = open(GUNICORN_CONF_SOURCE, 'r')
        template = Template(content.read())
        content.close()
        content = open(GUNICORN_FILE, 'w+')
        content.write(template.render(Context(DATA)))
        content.close()

        self.stdout.write('gunicorn file created successfuly\n')
