#!/usr/bin/env bash
sudo su
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install python3.9 -y
apt-get install python3-pip -y
pip3 install -U urllib3 requests
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2
update-alternatives  --set python3  /usr/bin/python3.9
pip3 install pipenv
pipenv install
export PATH="$HOME/.local/bin:$PATH"
