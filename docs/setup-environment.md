# Setup Environment

This page describes how to setup an environment to test the ACS playbook

NOTE: This page is for internal use only

## Prerequisites

* Python 3.8 installed


## Single Machine



## Multi Machine

Create Centos 7 EC2 instance using AMI from Marketplace
Install Git
Install Python3 "sudo yum install -y python3-pip"
sudo pip3 install ansible==2.9.13 molecule==3.0.8 molecule-ec2==0.2
git clone https://github.com/Alfresco/alfresco-ansible-deployment.git
cd alfresco-ansible-deployment
export TRAVIS_BUILD_NUMBER
export TRAVIS_BRANCH
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION
molecule create -s ec2multi


export MOLECULE_EPHEMERAL_DIRECTORY=/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2multi
python3 molecule/ec2multi/dynamic_inventory.py
cat inventory.yml
ansible all -m ping -i inventory.yml


export NEXUS_USERNAME
export NEXUS_PASSWORD
ansible-playbook -i inventory.yml playbooks/acs.yml