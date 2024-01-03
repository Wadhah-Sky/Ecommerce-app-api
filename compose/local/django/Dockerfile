# A Docker image is built up from a series of layers, each layer represents an instruction
# RUN, COPY, and ADD in the image’s Dockerfile, each layer except the very last one is read-only,
# commands that modify the filesystem create a layer.

# IMPORTANT: slim-bullseye (Debian 11) images DON'T come with networking-command line tools like (wget or curl).

# IMPORTANT: When trying to build your image within Docker swarm enviroment or in Docker engine
#            with swarm active, make sure that your image will not have a same user name that already
#            been use for another DUPLICATE image in same registery, otherwise could face:
#            1- 'Unable to lock database: Permission denied' error.
#            2- 'Failed to open apk database: Permission denied' error.
#            3- "adduser: user '<user name>' in use" error.

# Info: 'sed' linux command is a tool for replacing the text in a file, 'sed' is a stream editor
#       which means edit the file as a stream of characters.
#       Option '-i' comes in handy to edit the original file itself. If you use the '-i' option
#       the 'sed' command replaces the text in the original file itself rather than displaying it on
#       the terminal.
#       sed -i 's/\r$//g' , a command used to process the line endings of the shell scripts, which
#       converts Windows line endings to UNIX line endings.

# REMEMBER: for Python based images, make sure to set the default directory of your stage is where
#           'manage.py' file is holding.

# We are using 'multi-stage' building way.

# builder stage.
# Specify the docker image that your service build on.
FROM python:3.11.0b3-slim-bullseye AS builder

# Optional: Define maintainer.
MAINTAINER Wadhah Sky

# Set environment variable for ensuring that stdout and stderr are sent
# straight the container logs so we can see our application logs in real time.
# Note: Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Set environment variable for disabling the generation of bytecode.
# Note: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Copy the diffrent service start shell.
COPY /compose/local/django/es-index-rebuild.sh /usr/src/compose/es-index-rebuild.sh
COPY /compose/local/django/celery/worker/start-celeryworker.sh /usr/src/compose/start-celeryworker.sh
COPY /compose/local/django/celery/beat/start-celerybeat.sh /usr/src/compose/start-celerybeat.sh
COPY /compose/local/django/celery/flower/start-celeryflower.sh /usr/src/compose/start-celeryflower.sh

# Install os-level dependencies (as root).
RUN apt-get update && \
    # '--no-install-recommends' option, to avoid installing Recommended packages.
    # 'build-essential' dependencies for building Python packages.
    apt-get install -y -q --no-install-recommends build-essential \
    # postgress client (psycopg2) dependencies.
    libpq-dev \
    # proc file system utilities, in order to use pkill command.
    procps \
    # pillow required temporary dependencies.
    libjpeg-dev zlib1g-dev \
    # networking-command line tool.
    curl

# Note: adduser/addgroup command tool in slim-bullseye image has different options from alpine image.
# Install python virtual environemnt module 'venv', in Python based on linux Debian image hold the venv in '/opt/venv' file.
# To update pip:
# 1-  /opt/venv/bin/pip install --upgrade pip
# 2-  /opt/venv/bin/python3 -m pip install --upgrade pip
RUN python3 -m venv /opt/venv && \
    # update pip.
    /opt/venv/bin/python3 -m pip install --upgrade pip && \
    # create a user group 'usergroup' with group id. \
    # --system option, make addgroup tool add a system group.
    addgroup --gid 1001 --system usergroup && \
    # create a new user account with user id and add it to 'usergroup' on the image WITHOUT home directory
    # in order to use and run the application process only.
    # --system option make adduser tool create a system user. If a user with the same name already
    #   exists in the system uid range (or, if the uid is already used or if a user with that uid already exists),
    #   adduser will exit with a warning.
    # --no-create-home option will create a user without home directory. \
    # --disabled-password option tell adduser tool, Don't assign a password to this user. \
    # --gid option specify which group this user will belong to.
    adduser --uid 1001 --system --no-create-home --disabled-password --gid 1001 user && \
    # create 'static' directory.
    mkdir -p /usr/src/vol/web/static && \
    # create 'media' directory.
    mkdir -p /usr/src/vol/web/media && \
    # create directory for django logs.
    mkdir -p /var/log/django && \
    # Create file 'debug.log'.
    touch /var/log/django/debug.log && \
    sed -i 's/\r$//g' /usr/src/compose/es-index-rebuild.sh && \
    # Add the x permission which is the symbol for the execution permission. The execution
    # permission will give the execution ability to the owner user or group of the file.
    chmod +x /usr/src/compose/es-index-rebuild.sh && \
    sed -i 's/\r$//g' /usr/src/compose/start-celeryworker.sh && \
    chmod +x /usr/src/compose/start-celeryworker.sh && \
    sed -i 's/\r$//g' /usr/src/compose/start-celerybeat.sh && \
    chmod +x /usr/src/compose/start-celerybeat.sh && \
    sed -i 's/\r$//g' /usr/src/compose/start-celeryflower.sh && \
    chmod +x /usr/src/compose/start-celeryflower.sh && \
    # cleaning up unused and temp files to reduce the image size.
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

# div stage.
# use the 'builder' layer as base for this layer of the image.
FROM builder AS dev

# Copy from stage 'builder' what you need to use in this stage in case you are using different
# images for each stage.
#COPY --from=builder /opt/venv /opt/venv

# Copy the diffrent service start shell.
COPY /compose/local/django/start-django.sh /usr/src/compose/start-django.sh
# Copy source code from your project 'backend' directory to docker container 'backend' directory.
# Note: since there is no 'backend' directory in the image yet, will create it automatically.
COPY /backend /usr/src/backend

# install the required dependencies in 'requirements' file in python virtual environment.
RUN /opt/venv/bin/pip install -r /usr/src/backend/requirements.txt && \
    # change ownership of '/usr/src/compose/vol' directory and it's sub-folders using -R flag from 'root' user
    # to 'user' in 'usergroup' group.
    chown -R user:usergroup /usr/src/vol/ && \
    # change permission to allow for each digit:
    # owner: read(4)/write(2)/execute(1) =7, group: read/execute =5, more: read/execute =5
    chmod -R 755 /usr/src/vol/ && \
    chown -R user:usergroup /var/log/django/ && \
    chmod -R 766 /var/log/django/ && \
    sed -i 's/\r$//g' /usr/src/compose/start-django.sh && \
    chmod +x /usr/src/compose/start-django.sh

# Specify the default directory of this image layer (This should be where 'manage.py' file is holding or will be).
WORKDIR /usr/src/backend/django_rest

# Set environment variable for create Path variable for python virtual environemnt
# within image to use dependencies.
# Notw: PATH varaible tells the operating system where to find executables.
ENV PATH="/opt/venv/bin:$PATH"

# Switch docker container account from 'root' to the new account.
USER user

# production stage.
# use the 'builder' layer as base for this layer of the image.
FROM builder AS prod

# Copy the diffrent service start shell.
COPY /compose/production/django/start-django.sh /usr/src/compose/start-django.sh
# Copy source code from your project 'backend' directory to docker container 'backend' directory.
# Note: since there is no 'backend' directory in the image yet, will create it automatically.
COPY /backend /usr/src/backend

# install the required dependencies in 'requirements' file in python virtual environment.
RUN /opt/venv/bin/pip install -r /usr/src/backend/requirements.prod.txt && \
    # change ownership of '/usr/src/compose/vol' directory and it's sub-folders using -R flag from 'root' user
    # to 'user' in 'usergroup' group.
    chown -R user:usergroup /usr/src/vol/ && \
    # change permission to allow for each digit:
    # owner: read(4)/write(2)/execute(1) =7, group: read/execute =5, more: read/execute =5
    chmod -R 755 /usr/src/vol/ && \
    chown -R user:usergroup /var/log/django/ && \
    chmod -R 755 /var/log/django/ && \
    sed -i 's/\r$//g' /usr/src/compose/start-django.sh && \
    chmod +x /usr/src/compose/start-django.sh

# Specify the default directory of this image layer (This should be where 'manage.py' file is holding or will be).
WORKDIR /usr/src/backend/django_rest

# Set environment variable for create Path variable for python virtual environemnt
# within image to use dependencies.
# Notw: PATH varaible tells the operating system where to find executables.
ENV PATH="/opt/venv/bin:$PATH"

# Specify ports between the creator of the Docker image and the individual running the Container.
# Note: In recent versions of Dockerfile, EXPOSE doesn't have any operational impact anymore, it is just informative.
EXPOSE 8000

# Switch docker container account from 'root' to the new account.
USER user
