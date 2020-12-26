#!/bin/bash

/bin/python3 src/manage.py migrate
/bin/python3 src/manage.py runserver $1:$2