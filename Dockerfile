# A Docker image is built up from a series of layers, each layer represents an instruction
# in the image’s Dockerfile, each layer except the very last one is read-only, commands
# that modify the filesystem create a layer.

# Define the docker image.
FROM python:3.9-alpine

# Optional: Define maintainer.
MAINTAINER Wadhah Sky

# Specify python buffering mode.
ENV PYTHONUNBUFFERED 1

# Specify ports between the creator of the Docker image and the individual running the Container.
# EXPOSE 8000 5432

# Copy dependences names from your project source code to docker image 'requirements.txt' file.
COPY ./requirements.txt /requirements.txt

# Copy source code from your project 'app' directory to docker container 'app' directory.
# Note: since there is no 'app' directory in the image yet, will create it automatically.
COPY ./app /app

# Specify the default directory to run apps.
WORKDIR /app

# Install last version of 'PostgreSQL' client dependency that will be use by django through the driver 'psycopg2'
# to connect to Postgres server.
RUN apk add --update --no-cache postgresql-client

# Install image temporary dependencies those required while installing the requirements dependencies.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev

# install python virtual environemnt module 'venv', update pip and install the required dependences.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media

# Create path for python virtual environemnt on docker image system path.
ENV PATH="/py/bin:$PATH"

# Delete the temporary dependencies file.
RUN apk del .tmp-build-deps

# Create a new user account on docker image without home directory to use and run the application process only.
RUN adduser -D user

# Change ownership of '/vol' directory and it's subfolders using -R flag from 'root' user to
# 'user' in 'user' group.
RUN chown -R user:user /vol

# Change permission to allow everyone to read and execute the static files,
# the owner is allowed to write to the files as well.
RUN chmod -R 755 /vol

# Switch docker container account from 'root' to the new account.
USER user