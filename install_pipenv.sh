#!/usr/bin/env bash
sudo su
add-apt-repository ppa:deadsnakes/ppa
apt-get update

apt-get install python3.9 -y
apt-get install python3-pip -y
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2
update-alternatives  --set python3  /usr/bin/python3.9
sudo apt remove python3-apt
sudo apt autoremove
sudo apt autoclean
sudo apt install python3-apt
pip3 install pipenv
pipenv install
export PATH="$HOME/.local/bin:$PATH"
