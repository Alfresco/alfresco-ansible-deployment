#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install python3.9 -y
sudo apt-get install python3-pip -y
sudo pip3 install -U urllib3 requests
sudo pip3 install --user pipenv
export PATH="$HOME/.local/bin:$PATH"
pipenv shell
pipenv install