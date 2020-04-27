#!/bin/sh

if [ "$SQL_DATABASE" = "postgis" ]
then
    echo "Waiting for postgres..."

    while ! netcat -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Postgis started"
fi
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

