#!/bin/bash -e
curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | python3
cd /vagrant
python3 -m pipenv install --deploy
python3 -m pipenv run ansible-galaxy install -r requirements.yml
python3 -m pipenv run ansible-playbook -i inventory_local.yml -e "autogen_unsecure_secrets=true" playbooks/acs.yml
