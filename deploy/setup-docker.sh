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
       sudo service docker start
    fi

else

  echo "Installing Docker service!"
  echo "Step 1: Setup Docker's (apt) package manager repository..."
  echo "Add Docker's official GPG key"

  # The option -y to apt-get will automatically answer "yes" to prompts.
  sudo apt-get -y install ca-certificates curl gnupg

  sudo install -m 0755 -d /etc/apt/keyrings

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

  sudo chmod a+r /etc/apt/keyrings/docker.gpg

  echo "Add the repository to (apt) package manager sources"

  echo "deb [arch='$(dpkg --print-architecture)' signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu '$(. /etc/os-release && echo "$VERSION_CODENAME")' stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get -y update

  echo "Step 2: Install the Docker packages..."

  sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

  echo "Step 3: Verify Docker is installed successfully"

  sudo docker -v | grep -E "Docker version" || ehco "Docker is NOT installed successfully"

  echo "Step 4: Starting Docker service..."

  sudo service docker start

  echo "Done! :)"

fi

exit 0
