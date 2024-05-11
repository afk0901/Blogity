#!/bin/sh

python manage.py migrate && python manage.py test && exec python manage.py runserver 0.0.0.0:80
