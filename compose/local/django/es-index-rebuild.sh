#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Run start-django.sh script, and pulls in variables and functions from the
# the script (so they are usable from the calling script). It will of course
# run all the commands in called script, not only set variables. if you are
# using exit in called script, it will exit the first (calling) script as well,
# alternatively you can use:
#
# /bin/bash /path/to/scrip
#
# if you are using exit in called script, it will NOT exit the first script as
# well.

# source "${BASH_SOURCE[0]%/*}"/start-django.sh

# --------------------------------------------------------

python manage.py wait_for_es

echo "Re-build django documents into elasticsearch..."
# Execute the index re-build process of django documents into elasticsearch
# database.
sleep 15 && echo 'y' | python manage.py search_index --rebuild --no-parallel

echo "Re-build process is done!"

# Kill django runserver (ran by the called script)
# pkill -f runserver