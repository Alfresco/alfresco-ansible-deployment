# Deployment Guide

This page describes how to deploy the Alfresco Digital Business Platform (DBP) using Ansible.

The system deployed is shown in the diagram below.

TODO: Add diagram

## Components

TODO

## Prerequisites

* A CentOS machine (bare-metal or EC2 (ami-0affd4508a5d2481b)) to deploy to
* The machine needs to be able to access itself also trough its public location 
* SELinux httpd_can_network_connect should be set to 1 (allow)

## Deploy

1. Install Git
    ```bash
    sudo yum install -y git
    ```
2. Install Ansible
    ```bash
    sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    sudo yum install -y ansible
    ```
3. Clone the repository to the machine you wish to deploy to (How will we distribute the playbooks?)
    ```bash
    git clone https://github.com/Alfresco/alfresco-ansible-deployment.git
    # If you are using ssh
    # git clone git@github.com:Alfresco/alfresco-ansible-deployment.git
    ```
4. Navigate into the `acs-ansible-deployment` folder
5. Create a file called `inventory` with the following contents:
    ```
    [local]
    control ansible_connection=local
    ```
6. Navigate into the `playbooks` folder
7. Create a file called `nexus.yml` with the following contents (replacing the values appropriately):
    ```
    nexus_user: <your-username>
    nexus_password: <your-password>
    ```
8. Execute the playbook using the following command:
    ```bash
    ansible-playbook -i inventory playbooks/acs.yml
    ```
9. Access the system using the following URLs using a browser on the same machine:
    * Digital Workspace: ```http://alfresco.org/workspace```
    * Share: ```http://alfresco.org/share```
    * Repository: ```http://alfresco.org/alfresco```
    * Api-Explorer: ```http://alfresco.org/api-explorer```

## Configure

TODO

## Cleanup

TODO

## Troubleshooting

The best place to start if something is not working are the log files, these can be found in the following locations:

* Nginx 
    * `/var/log/nginx/error.log`
* Repository 
    * `/var/log/alfresco/alfresco.log`
    * `/var/log/alfresco/catalina.out`
* Share 
    * `/var/log/alfresco/share.log`

If you want to access the system from outside the playbook machine you will need to make sure you add an entry in /etc/hosts with "machineIp alfresco.org" on the pc you open the browser on.