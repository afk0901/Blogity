#!/bin/sh
python manage.py collectstatic --noinput --settings Bloggity.settings.production && \
python manage.py migrate --settings Bloggity.settings.production && \
exec gunicorn Bloggity.wsgi:application --bind 0.0.0.0:8080
# Uncomment this if testing locally with self signed certificates.
--certfile cert.pem --keyfile key.pem