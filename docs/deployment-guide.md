# Deployment Guide

This page describes how to deploy Alfresco Content Services (ACS) 6.2.x using Ansible.

The system deployed is shown in the diagram below.

![Single Machine Deployment](./resources/acs-single-machine.png)

## Prerequisites

* A CentOS 7 machine to deploy to, can be:
  * Bare Metal
  * Virtual Machine
  * EC2 instance (t3.large using ami-0affd4508a5d2481b in us-east-1)
* User running the playbook must have the ability to `sudo` any command

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

3. Clone the repository to the machine you wish to deploy to and switch to the stable tag:

    ```bash
    git clone https://github.com/Alfresco/alfresco-ansible-deployment.git
    cd alfresco-ansible-deployment
    git checkout tags/v1.0-A2
    ```

    > NOTE: As we protect the `Alfresco` organization with SAML SSO you will first have to authorize your SSH key or personal access token via [GitHub](https://github.com).

4. Create a file called `inventory` with the following contents in the `alfresco-ansible-deployment` folder:

    ```text
    [local]
    control ansible_connection=local
    ```

    > NOTE: This step won't be necessary in the future.

5. Create environment variables to hold your Nexus credentials as shown below (replacing the values appropriately):

    ```bash
    export NEXUS_USERNAME="<your-username>"
    export NEXUS_PASSWORD="<your-password>"
    ```

6. Execute the playbook as the current user using the following command (the playbook will escalate privileges when required):

    ```bash
    ansible-playbook -i inventory playbooks/acs.yml
    ```

    > NOTE: The playbook takes around 30 minutes to complete.

7. Access the system using the following URLs using a browser on the same machine:

    * Digital Workspace: ```/workspace```
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

## Known Issues

* The playbook is failing on CentOS 8
* The playbook downloads several large files so you will experience some pauses while they transfer and you'll also see the message "FAILED - RETRYING: Check on war download async task (nnn retries left)." appearing many times as the WAR file downloads
* The Tomcat access log is enabled by default and will grow in size quite quickly
* The playbook is not fully idempotent so may cause issues if you make changes and run many times

## Troubleshooting

The best place to start if something is not working are the log files, these can be found in the following locations:

* Nginx
  * `/var/log/alfresco/nginx.alfresco.error.log`
* Repository
  * `/var/log/alfresco/alfresco.log`
  * `/var/log/alfresco/catalina.out`
* Share
  * `/var/log/alfresco/share.log`
