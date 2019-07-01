#!/bin/bash

find */migrations/ -name '[0-9][0-9][0-9][0-9]*' -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth import get_user_model;
User = get_user_model(); User.objects.create_superuser(
'admin', 'admin@myproject.com', 'isamiiiko')" | python manage.py shell

