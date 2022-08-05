#!/bin/bash
sudo su
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install python3.9 -y
apt-get install python3-pip -y
pip3 install -U urllib3 requests
python3.9 -m pip install pipenv
cd /vagrant
pipenv install --dev
pipenv run ansible-galaxy install -r requirements.yml
pipenv run ansible-playbook -i inventory_local.yml playbooks/acs.yml
