#!/bin/bash -e
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9 python3.9-dev python3.9-distutils
curl -s -f https://bootstrap.pypa.io/get-pip.py | python3.9
python3.9 -m pip install pipenv
cd /vagrant
python3.9 -m pipenv install --deploy
python3.9 -m pipenv run ansible-galaxy install -r requirements.yml
python3.9 -m pipenv run ansible-playbook -i inventory_local.yml -e "autogen_unsecure_secrets=true" playbooks/acs.yml
