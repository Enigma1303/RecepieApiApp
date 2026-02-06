#!/bin/sh

set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
uwsgi --http :$PORT \
      --module app.wsgi \
      --master \
      --processes 4 \
      --threads 2


#python manage.py wait_for_db
#python manage.py collectstatic --noinput
#python manage.py migrate

#uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi