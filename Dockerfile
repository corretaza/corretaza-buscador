FROM ubuntu:14.04
RUN apt-get update
RUN apt-get install -y \
    libmysqlclient-dev \
    libtiff4-dev \
    libjpeg8-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.5-dev \
    tk8.5-dev \
    libxml2-dev \
    libxslt1-dev \
    xvfb \
    curl && \
    curl -sL https://deb.nodesource.com/setup | sudo bash -
RUN apt-get install -y \
    git \
    vim \
    nodejs \
    python-pip \
    python-dev \
    python-setuptools \
    python-tk \
    python-imaging \
    python-bs4 \
    python-pyside

# Install NODEJS and NPM + BOWER
#RUN npm -g install npm@latest && \
#    npm install -g bower

RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash
RUN npm install -g bower

ADD requirements/development.pip /
ADD requirements/base.pip /

RUN pip install -r development.pip && \
    rm -rf /var/lib/apt/lists/*
# Env do BD
ENV SEUCORRETOR_DB_NAME='seucorretor'
ENV SEUCORRETOR_DB_USER='root'
ENV SEUCORRETOR_DB_PASSWORD=''
ENV SEUCORRETOR_DB_HOST='192.168.99.1'

#Ajustar Timezone do Docker
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
     
COPY install/docker/scripts/build.sh /usr/local/bin/build
COPY install/docker/scripts/runserver.sh /usr/local/bin/runserver
RUN  chmod +x /usr/local/bin/runserver /usr/local/bin/build

EXPOSE 8000
