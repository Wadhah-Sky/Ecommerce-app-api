#!/bin/bash

<<comment

Any system consists of two main parts: 1- kernel, 2- userspace, the first one is responsible to deal
with hardware while the second one is where you interacts with system applications.

if you trying to execute a script in POSIX (Portable Operating System Interface) which is a set of
standard operating system interfaces based on the Unix...), the above line should be use in every
script to declare at its start the interpreter(like bash, sh or python) that is going to execute the
actual code. This is accomplished using the so called "shebang" line (that starts with #! characters and
the path to the bash or other interpreter of your choice).

If the kernel finds that the first two bytes are #! then it uses the rest of the line as an interpreter
and passes the file as an argument. So, to do this, the file needs to have execute permission:

chmod +x <file_name_path>

or as administrator:

sudo chmod +x <file_name_path>

comment

<<comment

getopt: is a C library function used to parse command-line options of the Unix/POSIX style.
It is a part of the POSIX specification, and is universal to Unix-like systems. It is also the
name of a Unix program for parsing command line arguments in shell scripts, the problem with this
tool is can't read long options (--option) only short (-option).

eval: command is used to execute the arguments as a shell command on unix or linux system. Eval
command comes in handy when you have a unix or linux command stored in a variable and you want to
execute that command stored in the string.

comment

<<comment
The "set" command is a built-in Linux shell command that displays and sets the names and values of
shell and Linux environment variables, The general syntax for the set command is:

set [options] [arguments]

* [options] are settings or flags that are "set" or "unset" in the Bash shell environment. Use it to
  influence the behavior of defined shell scripts and help execute the desired tasks:

    1- Set an option by using a minus sign (-) followed by the appropriate option.
    2- Unset an option by using a plus sign (+) followed by the appropriate option.

* [arguments] are positional parameters and they are assigned in order with the following parameters.
  When we pass arguments into the command line interface, a positional parameter is assigned to these
  arguments through the shell:

  $<1..9>

  you should know that argument $0 is represent the file itself, while $@ is represent all arguments
  from 1 to 9.

Note: Not specifying any options or arguments causes the command to print all shell variables.

Info: Shell functions dont really have "return values", just exit codes.
      The "set" command has three exit values:

        0. Marks a successful completion.
        1. Failure caused by an invalid argument.
        2. Failure resulting in a usage message, usually because an argument is missing.

comment

<<comment

The "set" command provides an extensive list of options that can be combined.
Most options have a corresponding -o flag that can be used to invoke the option.

The table below lists all options and their respective alternative form using the -o flag syntax:
* IMPORTANT: the options with value n/a means it only found in Bash shell.

 Options   	-o flags	                              Description
 _______    ________                  _____________________________________
  -a	     -o allexport	          Marks all created or modified variables or functions for export.
  -b	     -o notify	            Alerts the user upon background job termination.
  -e	     -o errexit	            Instructs a shell to exit if a command fails, i.e., if it outputs a non-zero exit status.
  -f	     -o noglob	            Disables filename generation (globbing).
  -h	     -o hashall	            Locates and saves function commands when a function is defined. The -h option is enabled by default.
  -k	     -o keyword	            Places all assignment arguments in the environment for a command, not just those preceding the
                                  command name.
  -n	     -o noexec	            Reads commands but doesnt execute them.
  -m	     -o monitor	            Displays a message when a task completes.
  -p	     -o privileged	        Disables the $ENV file processing and shell functions importing. The -p option is enabled
                                  by default when the real and effective user IDs dont match. Turning it off sets the effective uid
                                  and gid to the real uid and gid.
  -t	     -o onecmd	            Reads one command and then exits.
  -u	     -o nounset	            Treats unset or undefined variables as an error when substituting (during parameter expansion).
                                  Does not apply to special parameters such as wildcard * or @.
  -v	     -o verbose	            Prints out shell input lines while reading them.
  -x	     -o xtrace	            Prints out command arguments during execution.
  -B	     -o braceexpand	        Performs shell brace expansion.
  -C	     -o noclobber	          Prevents overwriting existing regular files by output redirection. By default, Bash allows
                                  redirected output to overwrite existing files.
  -E	     -o errtrace	          Causes shell functions to inherit the ERR trap.
  -H	     -o histexpand	        Enables style history substitution. The option is on by default when the shell is interactive.
  -P	     -o physical	          Prevents symbolic link following when executing commands.
  -T	     -o functrace	          Causes shell functions to inherit the DEBUG trap.
  n/a	     -o pipefail	          The return value of a pipeline is the status of the last command that had a non-zero status upon
                                  exit. If no command had a non-zero status upon exit, the value is zero.
  n/a	     -o posix	              Causes Bash to match the standard when the default operation differs from the Posix standard.

comment

set -o errexit
set -o nounset

<<comment

* The semi-colon(;) operator makes it possible to run, several commands in a single go and the execution of command occurs
  sequentially

In the bellow command we:
1- set -a : adds the export attribute to every variable that gets created on the linux system that run this script.
2- . .env : load .env file into memory of the linux system, here we assume that this script file is found in
            same directory where .env file is existing, otherwise we need to set the correct path to .env file.
3- set +a : restores the default behavior.

comment

set -a; . .env; set +a

# Define a function to be call when help option is been called or no arguments are provided,.
function usage() {
  # Using cat tool to print on the screen the following text.
  cat <<USAGE

  Usage: $0 [-c compose-file] [-s stack-name]

  Options:
      -c, --compose-file:   Specify the docker compose file to be use, i.e., docker-compose.yml,
                            default value is 'docker-compose.yml'.

      -s, --stack-name:     Specify a name to represent the stack that will deploy into docker swarm,
                            default value is 'ecommerce'.
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
STACK_NAME=

# We iterating through all arguments (flags) and its values of the command and use the 'shift' statement to
# remove the current argument or value, the while loop will breaks when there is no more argument left.
while [[ $# -gt 0 ]]; do
  case $1 in # Check argument value

    -c| --compose-file)
    DOCKER_COMPOSE_FILE=$2; # Save flag (argument) value
    shift;; # Remove --compose-file or -c from `$#`

    -s | --stack-name)
    STACK_NAME=$2; # Save flag (argument) value
    shift;; # Remove --stack-name or -s from `$#`

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

if [[ $STACK_NAME == "" ]]; then
    echo "Default value 'ecommerce' will be used as name to the stack name in docker swarm";
    STACK_NAME='ecommerce'
fi

# Run the 'docker stack deploy' command with the provided arguments value and by using the environment variables for
# docker-compose file from the system memory.
docker stack deploy --compose-file "$DOCKER_COMPOSE_FILE" --with-registry-auth "$STACK_NAME"