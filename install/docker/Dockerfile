FROM ubuntu:14.04

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Set debconf to run non-interactively
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update

# Install base dependencies
RUN apt-get install -y -q --no-install-recommends \
    apt-transport-https \
    build-essential \
    ca-certificates \
    curl \
    rsync \
    wget \
    git \
    vim \
    python-pip \
    python-dev \
    python-setuptools \
    python-tk \
    python-imaging \
    python-bs4

# Install MySQL, Pillow, LXML dependencies
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
    libxslt1-dev
#    python-pyside
#    xvfb \

# Install NodeJS, NPM, BOWER and GULP
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -yq nodejs
#RUN npm install -g npm
#RUN npm -g install npm@latest && \
RUN npm install -g bower gulp-cli

# Setup home environment
RUN mkdir /home/root && chown -R root: /home/root
RUN mkdir -p /home/root/bin /home/root/lib /home/root/include
ENV PATH /home/root/bin:$PATH

RUN mkdir /var/shared/
RUN chown -R root:root /var/shared
VOLUME /var/shared

WORKDIR /home/root
ENV HOME /home/root

# Link in shared parts of the home directory
RUN ln -s /var/shared/.ssh
RUN ln -s /var/shared/.bash_history
RUN ln -s /root/ corretaza-buscador
RUN chown -R root: /home/root
RUN touch .bashrc
RUN echo "alias ll='ls -alF'" >> .bashrc
RUN echo -n "PS1='\[\033[01;32m\]\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]" >> .bashrc && \
    echo -n '$(__git_ps1 " (%s)")' >> .bashrc && \
    echo -n " $ '" >> .bashrc

ADD requirements/development.pip /
ADD requirements/base.pip /
RUN cd / && pip install -r base.pip
RUN rm -rf /var/lib/apt/lists/*

# Env do BD
ENV SEUCORRETOR_DB_NAME='seucorretor'
ENV SEUCORRETOR_DB_USER='root'
ENV SEUCORRETOR_DB_PASSWORD=''
ENV SEUCORRETOR_DB_HOST='192.168.99.1'

#Ajustar Timezone do Docker
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY install/docker/scripts/build.sh /usr/local/bin/build
COPY install/docker/scripts/runserver.sh /usr/local/bin/runserver

RUN  chmod +x /usr/local/bin/runserver /usr/local/bin/build

EXPOSE 8000