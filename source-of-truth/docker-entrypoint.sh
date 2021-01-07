#!/bin/bash

/bin/python3 source_of_truth/manage.py migrate
/bin/python3 source_of_truth/manage.py runserver $1:$2