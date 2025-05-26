#!/bin/bash -e
sudo apt-get update -q

# Workaround for too old pipenv version in Ubuntu 22.04
if lsb_release -d | grep -q "Ubuntu 22.04"; then
  wget -q http://archive.ubuntu.com/ubuntu/pool/universe/p/pipenv/pipenv_2023.12.1+ds-1_all.deb -O /tmp/pipenv.deb
  sudo dpkg -i /tmp/pipenv.deb
else
  sudo apt-get install pipenv -qy
fi

cd /vagrant
python3 -m pipenv install --deploy
python3 -m pipenv run ansible-galaxy install -r requirements.yml
python3 -m pipenv run ansible-playbook -i inventory_local.yml \
  -e "acs_play_major_version=${VAGRANT_ACS_MAJOR_VERSION}" \
  -e "autogen_unsecure_secrets=true" \
  -e "acs_play_known_urls=[http://localhost]" \
  playbooks/acs.yml
