#!/bin/sh
python manage.py collectstatic --noinput --settings Bloggity.settings.production && \
python manage.py migrate --settings Bloggity.settings.production && \
exec gunicorn Bloggity.wsgi:application --bind 0.0.0.0:8080
# Comment this line in if testing locally.
#--certfile=./test_certs/cert.pem --keyfile=./test_certs/key.pem