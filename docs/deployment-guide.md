# Deployment Guide

This page describes how to deploy the Alfresco Content Services (ACS) using Ansible.

The system deployed is shown in the diagram below.

![Single Machine Deployment](./resources/acs-single-machine.png)


## Prerequisites

* A CentOS machine (bare-metal or EC2 (ami-0affd4508a5d2481b)) to deploy to
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
4. Navigate into the `alfresco-ansible-deployment` folder
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
    * Digital Workspace: ```/digital-workspace```
    * Share: ```/share```
    * Repository: ```/alfresco```
    * Api-Explorer: ```/api-explorer```

## Folder structure

You will find the Alfresco specific files in the following locations:
| Path   | Purpose   |
| ------ | --------- |
| ```/opt/alfrescp```     | Binaries - Alfresco Services and Dependencies |
| ```/etc/opt/alfresco``` | Configuration - Alfresco Services and Dependencies |
| ```/var/opt/alfresco``` | Data - Alfresco Services and Dependencies |
| ```/var/log/alfresco``` | Logs - Alfresco Services and Dependencies |


## Troubleshooting

The best place to start if something is not working are the log files, these can be found in the following locations:

* Nginx 
    * `/var/log/nginx/error.log`
* Repository 
    * `/var/log/alfresco/alfresco.log`
    * `/var/log/alfresco/catalina.out`
* Share 
    * `/var/log/alfresco/share.log`
