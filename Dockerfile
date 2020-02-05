# Dockerfile for Eficient-Learning-Khan experiment
FROM debian:stretch
MAINTAINER Paxton Fitzpatrick <paxton.c.fitzpatrick@dartmouth.edu
# created 2/5/2020

# install debian-related stuff
RUN apt-get update
RUN apt-get install -y eatmydata
RUN eatmydata apt-get install -y \
    python-dev \
    default-libmysqlclient-dev \
    python-pip \
    procps \
    git \
    curl \
    yasm
RUN rm -rf /var/lib/apt/lists/*

# install python packages
RUN pip install --upgrade pip
RUN pip install --upgrade \
setuptools \
requests \
mysql-python \
psiturk \
pydub \
matplotlib \
pandas \
numpy \
quail \
seaborn \
hypertools \
joblib \
sqlalchemy \
scipy \
deepdish \
datetime \
python-dateutil \
requests-oauthlib

# install vim
RUN apt-get update
RUN apt-get install -y vim

# add experiment and data folders
COPY exp /psiturk/exp

# setup working directory
WORKDIR /psiturk/exp

# set up psiturk to use the .psiturkconfig in /psiturk
ENV PSITURK_GLOBAL_CONFIG_LOCATION=/psiturk/

# expose port to access psiturk from outside
EXPOSE 22363
