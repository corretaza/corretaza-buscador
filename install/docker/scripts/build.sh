#!/usr/bin/env bash

cd /root/
pip install -r requirements/development.pip

# INSTALL PRIVATE REPOS
# OPTION 1 (you need permission)
# pip install -r requirements/extra.pip

# OPTION 2
cd /djapps/dj-corretaza-autoatendimento/ && python setup.py install
cd /djapps/dj-corretaza-pcorretor/ && python setup.py install
cd /djapps/dj-corretaza-pclientes/ && python setup.py install

export SEUCORRETOR_DB_NAME='seucorretor'
export SEUCORRETOR_DB_USER='root'
export SEUCORRETOR_DB_PASSWORD=''
export SEUCORRETOR_DB_HOST='192.168.99.1'

cd /root/ && bower install --allow-root

cd /root/seucorretor
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
