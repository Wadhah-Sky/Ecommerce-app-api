#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Remember: you should upload the last version of 'migration' files to Github repository before push it
#           production server.

# Note: since this script is will be used by container is not connected to local host, so any process that run
#       on container is related to that container, and this is the reason why we put 'makemigrations' process
#       here not like when we do in development where we use:
#
#       docker-compose -f docker-compose.yml run --rm app sh -c "python manage.py makemigrations"
#
#       which will write the new migrations file into local host that when we start 'app' service will be migrate
#       automatically.
#
#       So we do the following after make sure database is up and ready:
#       1- Create a new initial migrations for the apps.
#       2- Migrate the new created migrations files.

python manage.py wait_for_db

echo "Run the process to migrate the existing migrations files..."
echo yes | python manage.py migrate

# echo "Run the process to create new migrations files..."
# echo yes | python manage.py makemigrations

# echo "Run the process to migrate the migrations files to database..."
# echo yes | python manage.py migrate

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
echo yes | python manage.py collectstatic --clear

# Create super user depending on environment variables.
echo "Create superuser if not exists..."
python manage.py create-superuser

# Re-build indexes of elasticsearch engine.
/bin/bash /usr/src/compose/es-index-rebuild.sh

# In production we bind django server (import project) into gunicorn and We're
# running Gunicorn rather than the Django development server.
# Note: 'api' is name of directory that contains 'wsgi' file
# Info: if you want to use nginx server in the same container that run gunicorn, then you should run gunicorn as --daemon
#       which is only recommended in a Docker container when you have a programming that is a non-daemon process
#       (ie a program that runs continuously in the foreground).
gunicorn api.wsgi:application --bind 0.0.0.0:8000