#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

service_exists() {
  local n=$1
  if [[ $(systemctl list-units --all -t service --full --no-legend "$n.service" | sed 's/^\s*//g' | cut -f1 -d' ') == $n.service ]]; then
      return 0
  else
      return 1
  fi
}

echo "Checking if Docker service is already installed!"

if service_exists docker; then

    echo "is Docker service active?"

    if systemctl is-active docker | grep -E "active"; then
       echo "Yes, Docker is active, cancel installation process"
    else
       echo "No, Starting Docker service..."
       service docker start
    fi

else

  echo "Uninstall all Docker related conflicting packages!"
  # The option -y to apt-get will automatically answer "yes" to prompts.
  for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do apt-get remove -y $pkg; done

  echo "Update package manger..."

  apt-get update -y

  echo "Installing Docker service!"
  echo "Step 1: Setup Docker's (apt) package manager repository..."
  echo "Add Docker's official GPG key"

  # The option -y to apt-get will automatically answer "yes" to prompts.
  apt-get install -y ca-certificates curl gnupg

  install -m 0755 -d /etc/apt/keyrings

  # Note: The GPG keys are used to securely exchange information and verify the identity of the sender. GPG keys are
  #       often utilized in package management systems, email encryption, and software distribution in the Linux ecosystem
  #       to ensure data security and integrity.
  # Info: The GPG (GNU Privacy Guard) command in Linux is a powerful tool used for secure communication and data storage.
  #       The option -y to gpg command will automatically answer "yes" to prompts in case there is already
  #       '/etc/apt/keyrings/docker.gpg' file exists and will asking if you want to overwrite it or not.
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg -y --dearmor -o /etc/apt/keyrings/docker.gpg

  chmod a+r /etc/apt/keyrings/docker.gpg

  echo "Add the repository to (apt) package manager sources"

  # The 'tee' command, used with a pipe, reads standard input, then writes the output of a program to standard output
  # and simultaneously copies it into the specified file or files. Use the tee command to view your output immediately
  # and at the same time, store it for future use.

  # Note: if you want to check all the available releases of Docker engine to Ubuntu, check:
  #
  #       https://download.docker.com/linux/ubuntu

  # Info: with following command i have faced the following error:
  #
  #       The repository 'https://download.docker.com/linux/ubuntu 'mantic' Release' does not have a Release file.
  #
  #       I found out the mantic (version of my ubuntu) shouldn't be in quotes as well as the system architecture value
  #       within arch=<value>
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

  apt-get update -y

  echo "Step 2: Install the Docker packages..."

  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

  echo "Step 3: Verify Docker is installed successfully"

  docker -v | grep -E "Docker version" || ehco "Docker is NOT installed successfully"

  echo "Step 4: Starting Docker service, will take a minute..."

  sleep 60 && service docker start

  echo "Done! :)"

fi

exit 0
