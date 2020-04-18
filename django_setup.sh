#!/bin/sh

echo "Waiting for PostGIS Server to restart"
sleep 60

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

