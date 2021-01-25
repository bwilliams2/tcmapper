#! /bin/sh
if [ "$DATABASE" = "postgres_django" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 360
    done

    echo "PostgreSQL started"
fi

cd /webapp/backend

python manage.py flush --no-input

python manage.py migrate

gunicorn backend.wsgi:application --bind 0.0.0.0:8000