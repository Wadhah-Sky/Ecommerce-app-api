# IMPORTANT: alpine images come with networking-command line tools 'wget'.

# IMPORTANT: When no WORKDIR is specified, 'npm install' command to install package as local will
#            executed in the root directory (# or root) of the container, which is resulting an error:
#
#            npm ERR! Tracker "idealTree" already exists
#
#            So it's important when working with NodeJS images to specify WORKDIR before start using npm
#            to install packages locally.

# Info: 'yarn' and 'npm', when they detect an inconsistency between the project’s package.json
#        and the lockfile, they compensate for such change based on the package.json manifest by
#        installing different versions than those that were recorded in the lockfile.
#        This kind of situation can be hazardous for build and production environments as they
#        could pull in unintended package versions and render the entire benefit of a lockfile futile.
#        there is a way to tell both yarn and npm to adhere to a specified set of dependencies and their
#        versions by referencing them from the lockfile. Any inconsistency will abort the installation.
#        The command line should read as follows:
#
#        If you’re using Yarn, run 'yarn install --frozen-lockfile'.
#        If you’re using npm run 'npm ci'.

# Note: adduser/addgroup command tool in alpine image has different options from the other Debian images.

# Note: the npm global packages will stored in the image in:
#       /usr/local/lib/node_modules
#
#       while the local packages will stored in:
#       WORKDIRE/node_modules

# REMEMBER: The vue/Cli when run 'vue-cli-service serve' needs that the user who run the server has a home directory(~),
#           otherwise the docker contianer will exit with code 243.

# builder stage.
FROM node:18-alpine AS builder

MAINTAINER Wadhah Sky

# update to the latest stable version of npm globally in your system.
RUN npm install --location=global npm@latest && \
    # create a user group 'usergroup' with group id. \
    # --system option, make addgroup tool add a system group.
    addgroup -g 1001 -S usergroup && \
    # create a new user account and add it to 'usergroup' on the image WITHOUT home directory in order to create, use
    # and run the application process only.
    # -S option make adduser tool create a system user. If a user with the same name already exists in the system
    #    uid range (or, if the uid is already used or if a user with that uid already exists), adduser will exit
    #    with a warning.
    # -D option tell adduser tool, Don't assign a password to this user.
    # -H option will create a user without home directory.
    # -G assign the user to a group.
    adduser -u 1001 -S -D -G usergroup user

# div stage.
FROM builder AS dev

# Install Vue CLI globally, a full system for rapid Vue.js development, that provide 'vue create' command.
RUN npm install --location=global @vue/cli@5.0.8

# Copy the service start shell.
COPY /compose/local/vue/start-vue.sh /usr/src/compose/start-vue.sh
# Copy all your source code to the image.
COPY /frontend/vue_spa /usr/src/frontend/vue_spa

# Specify the default directory of this image layer (where 'node_modules' file is holding or will be).
WORKDIR /usr/src/frontend/vue_spa

# edit the original file itself as a stream of characters.
RUN sed -i 's/\r$//g' /usr/src/compose/start-vue.sh && \
    # Add execution permission to the file.
    chmod +x /usr/src/compose/start-vue.sh && \
    # change ownership of '/usr/' directory and its sub-directories using -R \
    # flag from 'root' user to 'user' in 'usergroup' group.
    chown -R user:usergroup /usr/src/ && \
    # in order to allow vue/cli to make directories (read/write/execute permission) in 'node_modules/.cache' directory,
    # Set specific permission for '/usr/src/' directory and its sub-directories to allow having for each digit:
    # owner(user): read(4)/write(2)/execute(1) =7, group: read/execute =5, more(other users): read/execute =5 \
    # otherwise will face issue when run 'run npm serve':
    #
    # error: vue-cli-service is not recognized as an internal or external command.
    #
    # Or when run command 'npm install', the bellow error will show:
    #
    # EACCES: permission denied, mkdir '/root/.cache/Cypress.
    #
    # Also if you are using nodemon tool to watch the directory, then will print:
    #
    # nodemon app crashed - waiting for file changes before starting...
    chmod -R 755 /usr/src/ && \
    # Install a tool that helps to automatically restarting the node application when file changes
    # in the directory are detected.
    # NOTE: this is a workaround since the hot-reload so far don't work on vue/cli@4.5 or later versions
    # when run on Docker.
    npm install --location=global nodemon

# Create path for npm dependencies of vue project in docker image system path.
# Note: bin file is hidden( set dot mark before it ).
ENV PATH="/usr/src/frontend/vue_spa/node_modules/.bin:$PATH"

# Specify ports between the creator of the Docker image and the individual running the Container.
EXPOSE 8080

# Switch docker container account from 'root' to the new account.
USER user

# Related to production stage:
# Copy all Vue *.json to docker image.
# NOTE: put backslash when trying to copy a file inside a directory.
# COPY /frontend/*.json /usr/src/frontend/
# install all npm packages on the system depending on package-lock.json file.
#    npm ci && \