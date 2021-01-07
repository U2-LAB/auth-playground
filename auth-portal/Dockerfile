FROM ubuntu:latest

# Update ubuntu
RUN apt-get update -y && apt-get upgrade -y

# Set docker args
ARG TIMEZONE

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

# Setup project
RUN mkdir /usr/src/auth-portal
COPY . /usr/src/auth-portal

ENV SECRET_KEY=ksdjflaklsdjfkajsdlkflajkl
ENV DJANGO_DB_NAME=auth_portal
ENV DJANGO_DB_USER=auth_portal_admin
ENV DJANGO_DB_PASSWORD=admin
ENV DJANGO_DB_HOST=db
ENV OAUTH_PATH=https://0.0.0.0:7000/oauth
ENV BASE_DATA_SERVICE_PATH=https://0.0.0.0:7000

# Update pip and install requirements
WORKDIR /usr/src/auth-portal/
RUN /bin/python3 -m pip install -U pip
RUN /bin/python3 -m pip install -r requirements.txt

# Give executed permission to entrypoint script
RUN chmod +x ./docker-entrypoint.sh

# Run app
CMD [ "./docker-entrypoint.sh", "0.0.0.0", "7000"]