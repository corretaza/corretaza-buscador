#!/usr/bin/env bash

cd /root/seucorretor/

./manage.py loaddata ../install/data/areadelazer.json
./manage.py loaddata ../install/data/condominios.json
./manage.py loaddata ../install/data/descricao_imoveis.json
./manage.py loaddata ../install/data/signup.json
./manage.py loaddata ../install/data/cidades.json
./manage.py loaddata ../install/data/descricao_comodos.json
./manage.py loaddata ../install/data/formadepagamento.json