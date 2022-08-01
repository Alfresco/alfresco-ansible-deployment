#!/usr/bin/env bash
pwd
ls -a
cat Pipfile
apt-get update
apt-get install python3.10 -y
apt-get install python3-pip -y
pip3 install -U urllib3 requests
pip3 install --user pipenv
export PATH="$HOME/.local/bin:$PATH"
pipenv install Pipfile