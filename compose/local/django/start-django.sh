#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py wait_for_db
python manage.py migrate
python manage.py wait_for_es
python manage.py runserver 0.0.0.0:8000