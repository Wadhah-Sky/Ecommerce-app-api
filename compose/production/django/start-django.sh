#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py wait_for_db
python manage.py migrate
python manage.py wait_for_es

# In production we bind django server (import project) into gunicorn and We're
# running Gunicorn rather than the Django development server.
# Note: 'api' is name of directory that contains 'wsgi' file
# Info: if you want to use nginx server in the same container that run gunicorn, then you should run gunicorn as --daemon
#       which is only recommended in a Docker container when you have a programming that is a non-daemon process
#       (ie a program that runs continuously in the foreground).
gunicorn api.wsgi:application --bind 0.0.0.0:8000