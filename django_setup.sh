#!/bin/sh

echo "Waiting for PostGIS Server to restart"
sleep 60

python manage.py makemigrations
python manage.py migrate

python manage.py shell -c "from users.models import User; User.objects.create_superuser('<ADMIN_EMAIL>', '<ADMIN_PASSWORD>')"
python manage.py loaddata init_data.json

python manage.py runserver 0.0.0.0:8000

