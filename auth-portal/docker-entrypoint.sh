#!/bin/bash

/bin/python3 auth-portal/manage.py migrate
/bin/python3 auth-portal/manage.py runserver $1:$2