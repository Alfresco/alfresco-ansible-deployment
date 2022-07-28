#!/usr/bin/env bash
apt-get update
apt-get install python3.10 -y
apt-get install python3-pip -y
pip3 install --user pipenv
pipenv install molecule
pipenv install Pipfile