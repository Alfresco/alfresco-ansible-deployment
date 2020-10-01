# Deployment Guide

This page describes how to deploy the Alfresco Content Services (ACS) using Ansible.

The system deployed is shown in the diagram below.

![Single Machine Deployment](./resources/acs-single-machine.png)

## Prerequisites

* A CentOS machine to deploy to, can be:
  * Bare Metal
  * Virtual Machine
  * EC2 instance (ami-0affd4508a5d2481b in us-east-1)

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

    ```text
    [local]
    control ansible_connection=local
    ```

6. Create environment variables to hold your Nexus credentials as shown below (replacing the values appropriately):

    ```bash
    export NEXUS_USERNAME=<your-username>
    export NEXUS_PASSWORD=<your-password>
    ```

7. Execute the playbook using the following command:

    ```bash
    ansible-playbook -i inventory playbooks/acs.yml
    ```

8. Access the system using the following URLs using a browser on the same machine:
    * Digital Workspace: ```/```
    * Share: ```/share```
    * Repository: ```/alfresco```

## Folder structure

You will find the Alfresco specific files in the following locations:
| Path   | Purpose   |
| ------ | --------- |
| ```/opt/alfresco```     | Binaries |
| ```/etc/opt/alfresco``` | Configuration |
| ```/var/opt/alfresco``` | Data |
| ```/var/log/alfresco``` | Logs |

## Troubleshooting

The best place to start if something is not working are the log files, these can be found in the following locations:

* Nginx
  * `/var/log/alfresco/nginx.alfresco.error.log`
* Repository
  * `/var/log/alfresco/alfresco.log`
  * `/var/log/alfresco/catalina.out`
* Share
  * `/var/log/alfresco/share.log`
