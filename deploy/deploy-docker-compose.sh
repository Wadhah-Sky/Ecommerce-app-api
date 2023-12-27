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
# Important: you don't have to worry about existing build version of images because docker will check if
#            it's the same image, will skip build process and pull it from local repository.

# If you want to build all docker images in one command (not recommended):
# docker compose -f $DOCKER_COMPOSE_FILE build

echo "Building Docker 'elk_setup' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build elk_setup

echo "Building Docker 'elasticsearch' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build elasticsearch

echo "Building Docker 'db' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build db

echo "Building Docker 'app' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build app

echo "Building Docker 'worker' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build worker

echo "Building Docker 'nginx' service image..."
docker compose -f $DOCKER_COMPOSE_FILE build nginx

echo "Process of building Docker services is Done and wait 30 seconds..."; sleep 30 && echo "Initialize and Start Docker containers in detach mode..."
# Note: I choose to run each service manually without using 'up' command with service profile.
# Important: you should run containers in detach mode so container run in background and not take the terminal
#            which lead to command run timeout error if there is another container want to run.

# Run elasticsearch service.
# Note: we prefer to use --profile flag to run 'elk_setup' service which defined as setup profile in order to solve
#       issue of network <name_of_network> is not found in case we run it separately.
echo "Run 'elasticsearch' service with profile..."; docker compose --profile -f $DOCKER_COMPOSE_FILE up -d elasticsearch

# Run the setup process for elasticsearch (this service has script to wait until elasticsearch service is ready,
# do its job and exit).
# Note: here we don't use detach mode to execute the up command of container because we up the container to
#       do a certain job and then exit.
# echo "Run 'elk_setup' service..."; docker compose -f $DOCKER_COMPOSE_FILE up elk_setup

# Run the database service.
echo "Run 'db' service and wait 30 seconds..."; docker compose -f $DOCKER_COMPOSE_FILE up -d db && sleep 30

# Create migration of your django service (app) apps models to the database:
# 1- Pretend to rollback all of your migrations without touching the actual tables in the project apps (you can
#    specify a certain app like, --fake core).
# 2- Remove your existing migration scripts for the apps. Where 'rm -rf' command is mostly used to remove
#    directories. As you will notice, this command uses two different options together.
#    The -r option indicates that the entire directory will be removed, while
#    the -f option indicates that this action will be forcefully performed.
# 3- Create a new initial migration for the apps.
# Note: here we don't use detach mode to execute the run command of container because we run the container to
#       do a certain job and then exit.
echo "Executing migration process of database..."
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py migrate --fake"
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "rm -rf migrations"
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py makemigrations"
echo "Migration process of database is Done."

echo "Create superuser in database if not exist..."
# Create super user depending on environment variables.
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py create-superuser"

# Collect static files of Django service (app)
# Note: --no-input flag means no for asking question of collectstatic to overwrite current static files.
#       --clear flag means clear the existing static files before creating the new ones.
echo "Collecting static files of Django to related volume..."
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py collectstatic --no-input --clear"

# Re-build indexes of elasticsearch engine.
echo "Run process of index re-build of Django documents to elasticsearch engine..."
docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "/usr/src/compose/es-index-rebuild.sh"

echo "Wait 30 seconds..."
sleep 30

# Run the other services.
echo "Run the rest of docker containers in detach mode..."
docker compose -f $DOCKER_COMPOSE_FILE up -d && echo "Your docker compose services is up!"

exit 0
