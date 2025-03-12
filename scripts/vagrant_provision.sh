#!/bin/bash -ex
sudo apt-get update -q
sudo apt-get install python3-pip -qy
cd /vagrant
pip install --user pipenv
python3 -m pipenv install --deploy
python3 -m pipenv run ansible-galaxy install -r requirements.yml
python3 -m pipenv run ansible-playbook -i inventory_local.yml \
    -e "acs_play_major_version=${VAGRANT_ACS_MAJOR_VERSION}" \
    -e "autogen_unsecure_secrets=true" \
    -e "acs_play_known_urls=[http://localhost]" \
    playbooks/acs.yml
