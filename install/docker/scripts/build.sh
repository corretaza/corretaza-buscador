#!/usr/bin/env bash
cd /root/

pip install -r requirements/development.pip

export SEUCORRETOR_DB_NAME='seucorretor'
export SEUCORRETOR_DB_USER='root'
export SEUCORRETOR_DB_PASSWORD=''
export SEUCORRETOR_DB_HOST='192.168.99.1'

bower install --allow-root

cd seucorretor/

./manage.py migrate

./manage.py runserver 0.0.0.0:8000
