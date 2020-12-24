FROM ubuntu:latest

# Update ubuntu
RUN apt-get update -y && apt-get upgrade -y

# Set docker args
ARG TIMEZONE
ARG DJANGO_SECRET_KEY

# Set current timezone
RUN ln -snf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime && echo ${TIMEZONE} > /etc/TIMEZONE

# Install dependencies 
RUN apt-get install -y curl tzdata build-essential checkinstall libssl-dev

# Install python packages 
RUN apt-get install -y \
 libreadline-gplv2-dev libncursesw5-dev \ 
  libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev\
   python3-dev python3-pip

# Install python
RUN apt-get install -y python3.9

# INSTALLING NODE
RUN curl -sL https://deb.nodesource.com/setup_lts.x && apt install -y nodejs npm

# Setup project
RUN mkdir /usr/src/business-app
COPY . /usr/src/business-app

# WORKDIR /usr/src/business-app/src/frontend
# RUN npm install -y
# RUN npm run build

WORKDIR /usr/src/business-app/src
RUN /bin/python3.9 -m pip install -U pip
RUN /bin/python3.9 -m pip install -r ../requirements.txt
