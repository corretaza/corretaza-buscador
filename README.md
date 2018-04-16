
INSTALL using docker
------------------

                          ##        .
                    ## ## ##       ==
                 ## ## ## ##      ===
             /""""""""""""""""___/ ===
        ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
             \______ o          __/
              \    \        __/
                \____\______/

1
--

    # create a target folder for the repos (IMPORTANT: use exaclty those paths)
    mkdir -p ~/workspacepy/ && cd ~/workspacepy/

    # clone the main repo (and open sourced)
    git clone -b staging https://github.com/corretaza/corretaza-buscador.git

    # clone the private repos (the secret sauces)
    git clone git@bitbucket.org:corretazadev/dj-corretaza-autoatendimento.git
    git clone git@bitbucket.org:corretazadev/dj-corretaza-pclientes.git
    git clone git@bitbucket.org:corretazadev/dj-corretaza-pcorretor.git


2
--

    # create the docker imagem
    cd corretaza-buscador
    docker build -t corretaza-buscador .


3
--

    # running
    # /root = volume for the main repo
    # /djapps = volume for the workspacepy that contains de private repos
    # /root/.ssh = host .ssh keys (that contains rsa keys for bitbucket private repos)
    docker run -ti -v $(pwd)/:/root -v ~/workspacepy:/djapps -v ~/.ssh/:/root/.ssh -p 8000:8000 corretaza-buscador bash

    # you need to install the 3 private repos...

    # ---> pip install -r /root/requirements/extra.pip
    # OR (do this for the 3 repos)
    cd /djapps/dj-corretaza-autoatendimento/ && python setup.py install

    # Load the sample data (ONE TIME ONLY)
    cd /root/install/docker/scripts/
    ./loaddata.sh 

    # Run Django
    cd root/seucorretor
    ./manage.py runserver 0.0.0.0:8000


Helps
-----

    # running using pre made scripts
    docker run -ti -v $(pwd)/:/root -p 8000:8000 corretaza-buscador build
    docker run -ti -v $(pwd)/:/root -p 8000:8000 corretaza-buscador runserver

    # LOGINs
    User: admin     Pwd: admin
    User: corretor  Pwd: corretor   ---> Agent
    User: gerente   Pwd: gerente    ---> Manager