#!/bin/sh

until PGPASSWORD=$SQL_PASSWORD psql --host=$SQL_HOST -U $SQL_USER ${SQL_DATABASE} -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done
echo "Database started"

set -e

python3 manage.py  collectstatic  --noinput
python3 manage.py  migrate  --noinput
echo "Database Migrated!"
python3 manage.py  shell   <  create_superuser.py
echo "Super User Created!"

gunicorn -w 4 -k uvicorn.workers.UvicornWorker plasma_for_covid.asgi:application --bind 127.0.0.1:8000
