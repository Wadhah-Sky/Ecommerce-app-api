#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Remember: you should upload the last version of 'migration' files to Github repository before push it
#           production server.

# Note: since this script is will be used by container is not connected to local host, so any process that run
#       on container is related to that container, So we do the following after make sure database is up and ready
#       and in order to track changes that happened or should happen:
#
#       1- To prevent confusion between local development database migrations and running production database,
#          delete all migrations files and create initial migrations file that the same on production server.
#       2- If you have any delete/add model fields, create new migrations file.
#       3- Push your source code to production server.
#       4- Migrate the migrations files in local and development server.

python manage.py wait_for_db

echo "Run the process to migrate the existing migrations files..."
echo yes | python manage.py migrate

# Collect static files of Django service (app).
# Note: --no-input flag means no for asking question of collectstatic to overwrite current static files.
#       --clear flag means clear the existing static files before creating the new ones.
#
# Note: echo yes is for question of You have requested to collect static files at the destination
#       ocation as specified in your settings:
#
#       /usr/src/vol/web/static
#
#       This will DELETE ALL FILES in this location! Are you sure you want to do this?
echo "Collect static files for django..."
sleep 10 &&
echo yes | python manage.py collectstatic --clear

# Create super user depending on environment variables.
echo "Create superuser if not exists..."
sleep 10 &&
python manage.py create-superuser

# Re-build indexes of elasticsearch engine.
sleep 10 &&
/bin/bash /usr/src/compose/es-index-rebuild.sh

sleep 10 &&
# In production we bind django server (import project) into gunicorn and We're
# running Gunicorn rather than the Django development server.
# Note: 'api' is name of directory that contains 'wsgi' file
# Info: if you want to use nginx server in the same container that run gunicorn, then you should run gunicorn as --daemon
#       which is only recommended in a Docker container when you have a programming that is a non-daemon process
#       (ie a program that runs continuously in the foreground).
gunicorn api.wsgi:application --bind 0.0.0.0:8000