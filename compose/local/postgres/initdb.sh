#!/usr/bin/env sh

set -o errexit
set -o nounset

# Note: This script file will be executed automatically by postgres after database have been initialized,
#       you should copy it into '/docker-entrypoint-initdb.d/' directory in your container image.

# This a command line to check if host is up.
#while true; do ping -c1 localhost > /dev/null && break; done

# 1- Must quote extension names or else symbolic error will be thrown.
# 2- Adds the extensions to database and tests database (template1)
PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
create extension if not exists "citext";
create extension if not exists "hstore";
\c template1
create extension if not exists "citext";
create extension if not exists "hstore";
select * FROM pg_extension;
EOSQL
