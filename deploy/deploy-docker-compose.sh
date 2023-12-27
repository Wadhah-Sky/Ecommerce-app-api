#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

# Define a function to be call when help option is been called or no arguments are provided,.
function usage() {
  # Using cat tool to print on the screen the following text.
  cat <<USAGE

  Usage: $0 [-c compose-file]

  Options:

      -c, --compose-file:   Specify the docker compose file to be use, i.e., docker-compose.yml,
                              default value is 'docker-compose.yml'.
USAGE
  exit 1
}

# if no arguments are provided, return usage function, if not able to call usage function then will
# exit and not continue the rest of script due 'exit 1'.
if [ $# -eq 0 ]; then
    usage
    exit 1
fi # end of if statement

# Define the the arguments those will represent the command flags (arguments).
DOCKER_COMPOSE_FILE=

# We iterating through all arguments (flags) and its values of the command and use the 'shift' statement to
# remove the current argument or value, the while loop will breaks when there is no more argument left.
while [[ $# -gt 0 ]]; do
  case $1 in # Check argument value

    -c| --compose-file)
    DOCKER_COMPOSE_FILE=$2; # Save flag (argument) value
    shift;; # Remove --compose-file or -c from `$#`

    -h| --help)
    usage;; # run usage function on help

    *) # Any other arguments.
    usage;; # run usage function if wrong argument provided

  esac # end of case statement
  shift # Remove argument's value from `$#`
done

# Check the flags values if empty or not.
if [[ $DOCKER_COMPOSE_FILE == "" ]]; then
    echo "Default value 'docker-dompose.yml' will be used as docker compose file";
    DOCKER_COMPOSE_FILE='docker-dompose.yml'
fi

# Important: in linux system, there is no 'docker-compose' command use 'docker compose'.

# First stop the current running docker services (in case there are) in given docker compose file,
# and remove them (only containers while volumes keep it).
echo "Stop Docker containers if running and remove any exist containers..."
docker compose -f $DOCKER_COMPOSE_FILE stop && docker compose -f $DOCKER_COMPOSE_FILE down

echo "Building Docker containers..."
# Build the given docker compose file service (only the ones who have build argument).

# If you want to build them in one command (not recommended)
# docker compose -f $DOCKER_COMPOSE_FILE build

echo "Building Docker 'elk_setup' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build elk_setup
echo "Building Docker 'elk_setup' service image is Done."

echo "Building Docker 'elasticsearch' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build elasticsearch
echo "Building Docker 'elasticsearch' service image is Done."

echo "Building Docker 'db' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build db
echo "Building Docker 'db' service image is Done."

echo "Building Docker 'app' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build app
echo "Building Docker 'app' service image is Done."

echo "Building Docker 'worker' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build worker
echo "Building Docker 'worker' service image is Done."

echo "Building Docker 'nginx' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build nginx
echo "Building Docker 'nginx' service image is Done."

echo "Process of building Docker services is Done and wait 30 seconds..."; sleep 30 && echo "Initialize and Start Docker containers..."
# Note: I choose to run each service manually without using 'up' command with service profile.

# Run elasticsearch service.
echo "Run 'elasticsearch' service..."; docker compose -f $DOCKER_COMPOSE_FILE up elasticsearch

# Run the setup process for elasticsearch (this service has script to wait until elasticsearch service is ready,
# do its job and exit).
echo "Run 'elk_setup' service..."; docker compose -f $DOCKER_COMPOSE_FILE up elk_setup

# Run the database service.
echo "Run 'db' service and wait 30 seconds..."; docker compose -f $DOCKER_COMPOSE_FILE up db && sleep 30

# Create migration of your django service (app) apps models to the database:
# 1- Pretend to rollback all of your migrations without touching the actual tables in the project apps.
# 2- Remove your existing migration scripts for the apps. Where 'rm -rf' command is mostly used to remove
#    directories. As you will notice, this command uses two different options together.
#    The -r option indicates that the entire directory will be removed, while
#    the -f option indicates that this action will be forcefully performed.
# 3- Create a new initial migration for the apps.
# 4- Fake a migration to the initial migration for the apps.
echo "Executing migration process of database..."
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py migrate --fake zero"
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "rm -rf migrations"
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py makemigrations"
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py migrate --fake"
echo "Migration process of database is Done."

echo "Create superuser in database if not exist..."
# Create super user depending on environment variables.
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py create-superuser"; echo "Superuser created successfully!"

# Collect static files of Django service (app)
# Note: --no-input flag means no for asking question of collectstatic to overwrite current static files.
#       --clear flag means clear the existing static files before creating the new ones.
echo "Collecting static files of Django to related volume..."
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py collectstatic --no-input --clear"

# Re-build indexes of elasticsearch engine.
echo "Run process of index re-build of Django documents to elasticsearch engine..."
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "/usr/src/compose/es-index-rebuild.sh"

echo "Wait 30 seconds..."

# Run the other services.
echo "Run the rest of docker containers..."
docker compose -f $DOCKER_COMPOSE_FILE up && echo "Your docker compose services is up!"

exit 0
