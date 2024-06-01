#!/bin/sh
python manage.py test && python manage.py migrate && exec python manage.py runserver \
--settings Bloggity.settings.production 0.0.0.0:80
