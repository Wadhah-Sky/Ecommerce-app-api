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

# Building stage.
FROM node:18-alpine AS builder

MAINTAINER Wadhah Sky

# Update package manger.
RUN apk update && \
    # update to the latest stable version of npm globally in your system.
    npm install --location=global npm@latest && \
    # Install Vue CLI globally, a full system for rapid Vue.js development, that provide 'vue create' command.
    npm install --location=global @vue/cli@5.0.8 && \
    # Make sure we got brotli plugin.
    apk add --upgrade brotli && \
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

# Devolopment stage.
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
    # change ownership of '/usr/' directory and its sub-directories using -R
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

# Prodduction stage.
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
COPY --from=dev /usr/src/frontend/vue_spa /usr/src/frontend/vue_spa
# COPY /frontend/vue_spa /usr/src/frontend/vue_spa

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

# Nginx building stage.
# Specify the docker image that your service build on.
FROM ubuntu:22.04 as Nginx

# Update package manger for Ubuntu
RUN apt update && \
    apt upgrade -y && \
    # Install required modules and plugins.
    # Module: a self-contained piece of software (e.g. types, data structure, functions, classes),
    #         that can be combined with other modules to construct a more complex software.
    # Plugin: a plugin is a ready to use software component that can be added to an existing
    #         software to change adds features.
    apt install -y libpcre3 libpcre3-dev zlib1g zlib1g-dev openssl libssl-dev wget git gcc make libbrotli-dev

# Specify the default directory of this image layer
WORKDIR /app

# Install Nginx compressed file and open it.
RUN wget https://nginx.org/download/nginx-1.25.3.tar.gz && tar -zxf nginx-1.25.3.tar.gz

# Clone using 'git' plugin the 'ngx_brotli' project.
# Note: If you pass --recurse-submodules to the git clone command, it will automatically initialize
#       and update each submodule in the repository, including nested submodules if any of the submodules
#       in the repository have submodules themselves.
RUN git clone --recurse-submodules -j8 https://github.com/google/ngx_brotli

# Move to nginx directrory
RUN cd nginx-1.25.3 && \
    # Run 'configure' script and pass ngx_brotli module path as value to argument '--add-dynamic-module'
    ./configure --with-compat --add-dynamic-module=../ngx_brotli && \
    # Compile the script of 'modules' file. \
    # Info: The 'make' command compiles different program pieces and builds a final executable.
    #       The purpose of make is to automate file compilation, making the process simpler and less
    #       time-consuming. The command works with any programming language as long as the compiler
    #       can be executed with a shell command.
    make modules

# Deployment stage.
# Specify the docker image that your service build on (nginx:1.25.3 is Debian distribute image).
FROM nginx:1.25.3 AS deploy

# Remove unnecessary directories and files.
# Note: this step should be before copying 'dist' folder and past it in 'html' folder,
#       otherwise will face issue of 'directory index of "/usr/share/nginx/html/" is forbidden'
#       when start/running Nginx.
RUN rm -rf /var/lib/apk/lists/* && \
    rm -rf /usr/share/nginx/html/index.html

# Get from 'Nginx' bulding stage the 'modules' file.
COPY --from=Nginx /app/nginx-1.25.3/objs/ngx_http_brotli_static_module.so /etc/nginx/modules/
COPY --from=Nginx /app/nginx-1.25.3/objs/ngx_http_brotli_filter_module.so /etc/nginx/modules/

# Get from 'prod' stage the 'dist' directory containst.
# Note: if you ever faced issue of HTTP 403 when trying to reach index.html through browser,
#       then it's issue with 'index.html' file, either it's not exist or one of static files can't be reach.
COPY --from=prod /usr/src/frontend/vue_spa/dist /usr/share/nginx/html/

# Copy the configuration file and mime.types
COPY /compose/production/nginx/start-nginx.sh /usr/src/compose/start-nginx.sh
COPY /compose/production/nginx/certbot.sh /usr/src/compose/certbot.sh
COPY /compose/production/nginx/ssl-options/ /etc/ssl-options
# Note: if you set file 'default.conf' as read_only (:ro) will lead to get 403 forbbiden.
COPY /compose/production/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY /compose/production/nginx/nginx.conf /etc/nginx/nginx.conf
COPY /compose/production/nginx/mime.types /etc/nginx/mime.types

# Update package manger
RUN apt-get update -y && \
    apt-get upgrade -y && \
    # Install:
    # 1- 'inotify-tools' so we have access to watch our certificates and trigger some actions when they change.
    # 2- With our configuration the certificates loaded into memory when nginx starts, we must ensure we have some
    #    certificates, even though dummy, when nginx starts so it doesn't complain about the missing files, and that’s
    #    why we will need 'openssl' which is is an all-around cryptography library that offers an open-source
    #    application of the TLS protocol. It allows users to perform various SSL-related tasks, including CSR
    #    (Certificate Signing Request) and private keys generation, and SSL certificate installation.
    # 3- 'certbot' is what we will need to actually emit valid ssl certificates.
    apt-get install -y inotify-tools openssl certbot && \
    sed -i 's/\r$//g' /usr/src/compose/start-nginx.sh && \
    chmod +x /usr/src/compose/start-nginx.sh && \
    sed -i 's/\r$//g' /usr/src/compose/certbot.sh && \
    chmod +x /usr/src/compose/certbot.sh && \
    chown -R 755 /var/log/ && \
    # Re-write 'brotli.conf' file withe required configuration.
    echo 'brotli on;\n \
          brotli_static on;\n \
          brotli_comp_level 11;\n \
          brotli_types application/atom+xml application/javascript application/json application/rss+xml\n \
          application/vnd.ms-fontobject application/x-font-opentype application/x-font-truetype\n \
          application/x-font-ttf application/x-javascript application/xhtml+xml application/xml\n \
          font/eot font/opentype font/otf font/truetype image/svg+xml image/vnd.microsoft.icon\n \
          image/x-icon image/x-win-bitmap text/css text/javascript text/plain text/xml;' > /etc/nginx/conf.d/brotli.conf && \
    # Run command to re-write 'nginx.conf' file with load_module of specific modules (Brotli) as 'nginx.conf' file.
    echo "load_module modules/ngx_http_brotli_filter_module.so;\nload_module modules/ngx_http_brotli_static_module.so;\n$(cat /etc/nginx/nginx.conf)" > /etc/nginx/nginx.conf

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
# CMD ["nginx", "-g", "daemon off;"]

# ------------------------------------------------------------------------------------
# Deployment stage if you want to use alpine abstract image.
# Specify the docker image that your service build on.
# If you want to use abstract image:
## FROM alpine AS deploy
# Note: we use Debain based image
# FROM nginx:1.24-alpine AS deploy

# Update package manger, for Debain is 'apt-get' and for Alpine is 'apk'
# RUN apk update && \
#    # Install the Brotli module package (is a lossless data compression algorithm originally
#    # developed by Google, and offers compression superior to gzip). BUT brotli package is not
#    # supported by default with Docker images and if you try to install it manually will face
#    # issues to load modules in 'nginx.conf' file.
#    # For Alpine is named: nginx-mod-http-brotli
#    # For Debian is named: nginx-plus-module-brotli \
#    # Remove unnecessary directories and files.
#    rm -rf /var/lib/apk/lists/* && \
#    rm -rf /usr/share/nginx/html/index.html

# COPY --from=prod /usr/src/frontend/vue_spa/dist /usr/share/nginx/html/
## COPY /frontend/vue_spa/dist /usr/share/nginx/html/

# COPY /compose/production/nginx/default.conf /etc/nginx/conf.d/default.conf
# COPY /compose/production/nginx/nginx.conf /etc/nginx/nginx.conf
# COPY /compose/production/nginx/mime.types /etc/nginx/mime.types

# WORKDIR /usr/share/nginx/html

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
# -------------------------------------------------------------------------------------