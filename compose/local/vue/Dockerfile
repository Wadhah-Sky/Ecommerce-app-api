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
    # Install Vue CLI globally, a full system for rapid Vue.js development, that provide 'vue create' command.
    npm install --location=global @vue/cli@5.0.8 && \
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
# RUN npm install --location=global @vue/cli@5.0.8

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

# Switch docker container account from 'root' to the new account.
USER user

# prodduction stage.
# Note: in production stage of Vue, you need 'dist' file only which contains all static files to be
#       served, either by django directly or through Nginx, So, you don't need docker container to serve Vue
#       files, all what you need is copy 'dist' file into the mentiod servers, or you can simply
#       A- add 'dist' file to GitHub repository of your project, then make Django or Nginx copy 'dist' within
#          their 'static' directory.
#       B- add 'dist' file to your Django application 'static' directory (make sure it's defined in 'STATICFILES_DIRS'
#          in settings.py file) and then run withing Django container:
#
#          python manage.py collectstatic --no-input --clear
FROM builder AS prod

# Copy all Vue *.json to docker image.
# COPY /frontend/vue_spa/*.json /usr/src/frontend/vue_spa/

# Copy all your source code to the image.
COPY /frontend/vue_spa /usr/src/frontend/vue_spa

# Specify the default directory of this image layer (where 'node_modules' file is holding or will be).
WORKDIR /usr/src/frontend/vue_spa

# install all npm packages on the system depending on package-lock.json file.
RUN npm ci && \
    # Build 'dist' optimized file that Compiled and minified for production.
    npm run build && \
    # Delete all directories recursively except 'dist' using 'find' command:
    # Note: you can use -type f to delete files.
    find . -maxdepth 1 -type d -not -name 'dist' -delete

# Switch docker container account from 'root' to the new account.
USER user

# deployment stage.
# Specify the docker image that your service build on.
FROM nginx:1.25-alpine AS deploy

# Update package manger.
RUN apk update && \
    # Remove unnecessary directories and files.
    rm -rf /var/lib/apk/lists/* && \
    rm -rf /usr/share/nginx/html/index.html

# Get from 'prod' stage the 'dist' directory containing.
COPY --from=prod /usr/src/frontend/vue_spa/dist /usr/share/nginx/html/
# COPY /frontend/vue_spa/dist /usr/share/nginx/html/

# Copy the configuration file and mime.types
# Note: if you set file 'default.conf' as read_only (:ro) will lead to get 403 forbbiden.
COPY /compose/production/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY /compose/production/nginx/nginx.conf /etc/nginx/nginx.conf
COPY /compose/production/nginx/mime.types /etc/nginx/mime.types

# Specify the default directory of this image layer (where 'node_modules' file is holding or will be).
WORKDIR /usr/share/nginx/html

# EXPOSE 80

# Run nginx and run it in a non-background (daemon) mode, Nginx image container by default it start nginx server
# with daemon off.
# Note: Docker has a default entrypoint which is /bin/<default_terminal> -c but does not have a default command.
#       The 'ENTRYPOINT' specifies a command that will always be executed when the container starts.
#       The 'CMD' specifies arguments that will be fed to the ENTRYPOINT.
#       For example:
#
#       ENTRYPOINT ["/bin/ping"]
#       CMD ["localhost"]
CMD ["nginx", "-g", "daemon off;"]