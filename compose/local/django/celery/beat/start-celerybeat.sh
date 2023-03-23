#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A api beat -l INFO