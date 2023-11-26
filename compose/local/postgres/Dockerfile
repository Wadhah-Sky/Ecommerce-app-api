# IMPORTANT: you can set Default Docker Environment Variables During Image Build, even can overwrite the default ones
#            using docker or docker-compose command:
#
#            docker-compose build --build-arg buildtime_variable=a_value another_buildtime_variable=a_value

# Info: by defualt PostgrsSQL will create (unprivileged) user that will own the server process called 'postgres', but
#       since we configured Dockerfile manually, so it's required to log in as (unprivileged) user at the end.

# Note: If you set POSTGRES_HOST_AUTH_METHOD/POSTGRES_INITDB_ARGS to be:
#       1- 'trust' value, then POSTGRES_PASSWORD is not required.
#       2- 'scram-sha-256' value, then POSTGRES_PASSWORD is required.
#       3- 'peer' value, require the same username in the operating system as
#           in PostgreSQL, use 'peer' (UNIX, only for local connections) or 'sspi'
#           (Windows).

# Info: if ever faced such an error:
#
#        psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432"
#        failed: No such file or directory
#
#        1- This means you have an issue with authentication when this script is run, usually due to
#           password requesting.
#        2- Or you are trying to run script file or command before the postgres server is initialized.

# Note: if you faced an error 'permission denied' and you where using unprivileged user, this is because
#       you have create that user upon a layer that didn't have that user file, and so you have to delete
#       the container and re-build it again.

# builder stage.
# Specify the docker image that your service build on.
FROM postgres:14-alpine AS builder

# Optional: Define maintainer.
MAINTAINER Wadhah Sky

# Copy the initdb_extensions script to the image.
COPY /compose/local/postgres/initdb.sh  /docker-entrypoint-initdb.d/initdb.sh

RUN addgroup -g 1001 -S usergroup && \
    adduser -u 1001 -S -D -G usergroup user && \
    sed -i 's/\r$//g' /docker-entrypoint-initdb.d/initdb.sh && \
    chmod +x /docker-entrypoint-initdb.d/initdb.sh

# Set default arguments for environment variables.
ARG BUILDTIME_PGDATA=/var/lib/postgresql/data
ARG BUILDTIME_POSTGRES_DB=postgres
ARG BUILDTIME_POSTGRES_USER=postgres
ARG BUILDTIME_POSTGRES_PASSWORD=1234
ARG BUILDTIME_POSTGRES_HOST_AUTH_METHOD=scram-sha-256
ARG BUILDTIME_POSTGRES_INITDB_ARGS="--auth-local=scram-sha-256 --auth-host=scram-sha-256 --data-checksums"

# Set directory value other from the default one that 'initdb' command use to create databases cluster in.
ENV PGDATA=$BUILDTIME_PGDATA
# Set the default database name that will created by 'initdb' at the time create the cluster.
ENV POSTGRES_DB=$BUILDTIME_POSTGRES_DB
# Set the user name vaule for database that will use when trying to connect to the database.
ENV POSTGRES_USER=$BUILDTIME_POSTGRES_USER
# Set the password for that username.
ENV POSTGRES_PASSWORD=$BUILDTIME_POSTGRES_PASSWORD
# Set Authentication method to control the 'auth-method' for host connections for all databases, all users, and all addresses.
# If unspecified then 'scram-sha-256' password authentication is used.
ENV POSTGRES_HOST_AUTH_METHOD=$BUILDTIME_POSTGRES_HOST_AUTH_METHOD
# Set optional arguments to be use when 'initdb' command is executed to create the cluster.
# You should set these arguments like you set them directly to the command, means in form of '--argument=value'.
ENV POSTGRES_INITDB_ARGS=$BUILDTIME_POSTGRES_INITDB_ARGS

# div stage.
FROM builder AS dev

RUN chown -R user:usergroup /var/ && \
    chmod -R 755 /var/

WORKDIR /var/lib/postgresql/data

# EXPOSE 5432

# log in as the (unprivileged) user that will own the server process, otherwise will face issue
# to run 'initdb' command.
USER user

# Note: no need to the following command because postgres automatically execute 'initdb.sh' when
#       docker container is started.
#CMD ["sh", "/docker-entrypoint-initdb.d/initdb.sh"]

# production stage.
FROM builder AS prod

RUN chown -R user:usergroup /var/ && \
    chmod -R 755 /var/

WORKDIR /var/lib/postgresql/data

# EXPOSE 5432

# log in as the (unprivileged) user that will own the server process, otherwise will face issue
# to run 'initdb' command.
USER user

# for production, start an existing server.
# Note: 'pg_ctl start' command lead to start the server and then exit with 0.
# CMD pg_ctl -D /var/lib/postgresql/data -l logfile start