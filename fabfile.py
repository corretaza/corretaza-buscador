##
## You MUST update the following ## UPDATE HERE areas
##

import platform
from fabric.api import env, sudo, run, cd, prefix, require
from fabric.colors import green, red
from fabric.utils import abort

from os import environ, pardir
from os.path import abspath, basename, dirname, join, normpath, exists, isdir
from sys import path

BASE_DIR = dirname(__file__)  #Project or Repo Base Dir
VIRTUALENV_DIR = dirname(dirname(__file__))

REPO_FOLDER_NAME = 'seucorretor_repo'
PROJECT_NAME = 'seucorretor'

## UPDATE HERE: Enter below the repository URL that will receive your new project code
PROJECT_REPO = 'git@bitbucket.org:huogerac/seucorretor.git'

## Here are the default NGINX and UPSTAR directories
NGINX_TARGET_FOLDER = '/etc/nginx'
GUNICORN_TARGET_FOLDER = '/etc/init'



#Pre requirements:
#nodejs npm bower --> django-bower
#Pillow --> ckeditor http://pillow.readthedocs.org/en/latest/installation.html
#lxml (beautifulsoup4) --> http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
#                      --> http://stackoverflow.com/questions/6504810/how-to-install-lxml-on-ubuntu

SO_PACKAGES = {'Linux': {'cmd_install': "apt-get -y install",
                         'basic':[],
                         'project':["libxml2-dev libxslt1-dev python-dev "], # python-lxml
                         'pillow':["libtiff4-dev", "libjpeg8-dev", "zlib1g-dev", "libfreetype6-dev", "liblcms2-dev", "libwebp-dev", "tcl8.5-dev", "tk8.5-dev", "python-tk",],
                         'development':[],
                         'staging':["nginx",],
                         'extra_cmd': "npm install -g bower"
                        },
               'Darwin':{'cmd_install': "brew install",
                         'basic':[],
                         'project':[],
                         'pillow':["libtiff", "libjpeg", "webp", "little-cms2",],
                         'development':[],
                         'staging':["nginx",],
                         'extra_cmd': "npm install -g bower"
                        }

              }

#'project':["libgraphviz-dev", "graphviz", "python-pygraphviz",],

#MYSQL "libmysqlclient-dev", "mysql-client", "python-mysqldb",

def __get_env_pass__(environment):
    pass_env_var_name = '%s_%s' % (PROJECT_NAME.upper(), environment.upper())
    pass_env_var = environ.get(pass_env_var_name)
    if not pass_env_var:
        abort('You must set up the password using the SO variable: %s' % pass_env_var_name)
    return pass_env_var

def development():
    "Setup development (local) instance"
    env.environment = 'development'
    env.dev_mode = True
    env.hosts = ["localhost", ]
    env.server_url = 'localhost:8000'
    ## UPDATE HERE: Enter below your development workspace directory
    env.targetdir = '~/workspacepy/myprojects'


def staging():
    "Setup staging server"
    env.environment = 'staging'
    env.dev_mode = False
    ## UPDATE HERE: Enter below the staging server DOMAIN
    env.hosts = ["seucorretor.na-inter.net", ]
    env.server_url = 'seucorretor.na-inter.net'
    ## UPDATE HERE: Enter below a valid user that has SSH access to the above server
    env.user = 'mechanics'
    env.password = __get_env_pass__('staging')
    ## UPDATE HERE: Enter below the staging directory where the virtualenv will be created
    env.targetdir = '/home/mechanics/envs'


def production():
    "Setup production server"
    env.environment = 'production'
    env.dev_mode = False
    ## UPDATE HERE: Enter below the staging server DOMAIN
    env.hosts = ["valeimoveissjc.com.br", ]
    env.server_url = 'valeimoveissjc.com.br'
    ## UPDATE HERE: Enter below a valid user that has SSH access to the above server
    env.user = 'mechanics'
    env.password = __get_env_pass__('production')
    ## UPDATE HERE: Enter below the staging directory where the virtualenv will be created
    env.targetdir = '/home/mechanics/envs'


def _install_so_dependencies():
    system = platform.system()
    print(green("**** Installing SO (%s) dependencies" % system))

    cmd_install = SO_PACKAGES[system]['cmd_install']
    extra_cmd = SO_PACKAGES[system]['extra_cmd']

    basic_packages = " ".join(SO_PACKAGES[system]['basic'])
    project_packages = " ".join(SO_PACKAGES[system]['project'])
    pillow_packages = " ".join(SO_PACKAGES[system]['pillow'])
    environment_packages = " ".join(SO_PACKAGES[system][env.environment])

    print(green("Installing Basic packages"))
    sudo("%s %s" % (cmd_install, basic_packages))

    print(green("Installing Project packages"))
    sudo("%s %s" % (cmd_install, project_packages))

    print(green("Installing Pillow packages"))
    sudo("%s %s" % (cmd_install, pillow_packages))    

    print(green("Installing Enviroment packages"))
    sudo("%s %s" % (cmd_install, environment_packages))

    print(green("Installing Extra packages"))
    sudo("%s" % extra_cmd)


def _create_virtualenv(targetdir, virtualenv_folder):
    print(green("**** Creating virtualenv"))
    with cd(targetdir):
        run("virtualenv %s" % virtualenv_folder)

def _clone_repository(targetdir, virtualenv_folder ):
    print(green("**** Cloning Repository"))
    with cd(targetdir):
        run("cd %s; git clone %s %s" % (virtualenv_folder, PROJECT_REPO, REPO_FOLDER_NAME))

def _install_project_dependencies(projectdir):
    print(green("**** Installing project dependencies"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('pip install -r ../requirements/%(environment)s.pip' % env)
            run('./manage.py bower_install --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))

def _prepare_database(projectdir):
    print(green("**** Preparing Database"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py syncdb --noinput --no-initial-data --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))
            run('./manage.py migrate --all --no-initial-data --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))
            run('./manage.py migrate --all --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))


def _generate_nginx_entry(projectdir):
    print(green("**** Preparing NGINX entry"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py nginxentry --env %s --url %s --nginx %s --settings=%s.settings.%s' % (env.environment, env.server_url, NGINX_TARGET_FOLDER, PROJECT_NAME, env.environment))


def _generate_gunicorn_entry(projectdir):
    print(green("**** Preparing GUNICORN entry"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py gunicornentry --env %s --user %s --settings=%s.settings.%s' % (env.environment, env.user, PROJECT_NAME, env.environment))

def _enable_nginx(projectdir):
    print(green("**** Enableing NGINX"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py nginxenable --env %s --nginx %s --settings=%s.settings.%s' % (env.environment, NGINX_TARGET_FOLDER, PROJECT_NAME, env.environment))

def _prepare_log_folder(targetdir, virtualenv_folder):
    print(green("**** Preparing Log folder"))
    with cd(targetdir):
        run('mkdir -p %s/logs' % virtualenv_folder)


def bootstrap():
    print(green("Bootstrap:: targetdir=%s" % env.targetdir))

    virtualenv_folder = "%s_%s" % (PROJECT_NAME, env.environment)
    repodir = join(env.targetdir, virtualenv_folder, REPO_FOLDER_NAME)
    projectdir = join(repodir, PROJECT_NAME)

    #_install_so_dependencies()
    _create_virtualenv(env.targetdir, virtualenv_folder)
    _clone_repository(env.targetdir, virtualenv_folder)
    _install_project_dependencies(projectdir)
    _prepare_database(projectdir)
    if not env.dev_mode:
        _generate_nginx_entry(projectdir)
        _generate_gunicorn_entry(projectdir)
        _enable_nginx(projectdir)
        _prepare_log_folder(env.targetdir, virtualenv_folder)

    print(green("bootstrap DONE"))




def _update_code(projectdir):
    print(green("**** Updating repository"))
    with cd(projectdir):
        run("git pull")

def _migrate_database(projectdir):
    print(green("**** Migrating Database"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py migrate --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))

def _update_assets(projectdir):
    print(green("**** Updating Assets (static files)"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py collectstatic --noinput --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))

def _reload_servers():
    print(green("**** Reloading servers (NGINX, GUNICORN"))
    GUNICORN_SERVICE = "gunicorn-%s_%s" % (PROJECT_NAME, env.environment)
    NGINX_SERVICE = "nginx"
    try:
        sudo("reload %s" % GUNICORN_SERVICE)
    except:
        sudo("start %s" % GUNICORN_SERVICE)
    sudo("service %s reload" % NGINX_SERVICE)


def deploy():
    print(green("Deploying :: %s (%s)" % (env.environment, env.hosts)))

    virtualenv_folder = "%s_%s" % (PROJECT_NAME, env.environment)
    repodir = join(env.targetdir, virtualenv_folder, REPO_FOLDER_NAME)
    projectdir = join(repodir, PROJECT_NAME)

    _update_code(projectdir)
    _install_project_dependencies(projectdir)
    _migrate_database(projectdir)
    if not env.dev_mode:
        _update_assets(projectdir)
        _reload_servers()
    
    print(green("Deploy DONE"))
