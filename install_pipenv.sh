#!/usr/bin/env bash
apt-get update
apt-get install python3.10 -y
apt-get install python3-pip -y
pip3 install -U urllib3 requests
pip3 install --user pipenv
echo -e 'export PATH="$PATH:/Library/Frameworks/Python.framework/Versions/3.9/bin"' >> $HOME/.bash_profile
export PATH="$HOME/.local/bin:$PATH"
cat Pipfile
pwd
pipenv install Pipfile
echo test4