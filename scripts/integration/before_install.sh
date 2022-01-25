#!/bin/bash -e
openssl aes-256-cbc -K $encrypted_6c8b9ee48a27_key -iv $encrypted_6c8b9ee48a27_iv \
    -in alfresco-ansible.pem.enc -out /tmp/dbp-ansible -d

eval "$(ssh-agent -s)"
chmod 600 /tmp/dbp-ansible
ssh-add /tmp/dbp-ansible

curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
./awscli-bundle/install -b ~/bin/aws

export PATH=~/bin:$PATH
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export AWS_DEFAULT_REGION='us-east-1'

git clone --depth 1 --branch $DTAS_VERSION https://$GITHUB_TOKEN@github.com/Alfresco/alfresco-deployment-test-automation-scripts.git dtas
