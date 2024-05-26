#!/bin/sh
python manage.py test && python manage.py migrate && exec python manage.py runserver 0.0.0.0:80
