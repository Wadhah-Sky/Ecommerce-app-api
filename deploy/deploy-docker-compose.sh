#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

# Important: don't put && after command that not return 0 or 1 exit value and can be fail because your will
#            force the command behind to run.

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
# Note: we execute 'down' command twice in case first attempt didn't delete all containers and its resource (like network).
echo "Stop Docker containers if running and remove any exist containers..."
docker compose -f $DOCKER_COMPOSE_FILE stop && sleep 50 && docker compose -f $DOCKER_COMPOSE_FILE down && sleep 30 && docker compose -f $DOCKER_COMPOSE_FILE down

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
# Important: Don't run migration process before database is ready, because will cause an issue for packages
#            that depends on migration process like 'django-admin-interface' and its error:
#
#            django.db.utils.ProgrammingError: relation "admin_interface_theme" does not exist
#
echo "Run 'db' service and wait 30 seconds..."; docker compose -f $DOCKER_COMPOSE_FILE up -d db && sleep 30

# echo "Installing default django theme..."
# Note: no need to this step but in case you want to install different theme you should do it development PC so the
#       new files loaded to Github repository and here only collect it.
# docker compose -f $DOCKER_COMPOSE_FILE run --rm app sh -c "python manage.py loaddata admin_interface_theme_django.json" && sleep 10

# Run 'app' service in detach mode that will make sure database is updated.
# Important: since we are not using 'root' user (privileges), so we can't use 'rm' command and will return permission
#            denied.
echo "Run 'app' service and wait 30 seconds..."
docker compose -f $DOCKER_COMPOSE_FILE up -d app && sleep 30

echo "Run 'nginx' service and wait 10 seconds..."
docker compose -f $DOCKER_COMPOSE_FILE up -d nginx && sleep 10

# Run the other services.
echo "Run the rest of docker containers in detach mode..."
docker compose -f $DOCKER_COMPOSE_FILE up -d && echo "Your docker compose services is up!"

echo "Wait 10 seconds before exit..."
sleep 10

exit 0