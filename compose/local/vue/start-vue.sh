#!/bin/sh

set -o errexit
set -o nounset

: '
Specify the default command to run whenever the service image is run within container
while no commands were provided.
Note: execute the command to run development server of vue/cli using nodemon, after
specify the files to track and to watch only, in my case only want "src" file of vue
application to watch, and track changes in files with .js, .css or .vue extension.
 '

nodemon --ext js,css,vue --watch src --exec npm run serve