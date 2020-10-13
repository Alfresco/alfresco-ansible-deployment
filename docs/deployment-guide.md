# Deployment Guide

This page describes how to deploy Alfresco Content Services (ACS) 6.2.x using Ansible.

The system deployed is shown in the diagram below.

![Single Machine Deployment](./resources/acs-single-machine.png)

## Prerequisites

* A CentOS machine to deploy to, can be:
  * Bare Metal
  * Virtual Machine
  * EC2 instance (t3.large using ami-0affd4508a5d2481b in us-east-1)
* SELinux is disabled

  This can be achieved by running the following command:

  ```bash
  sudo setenforce 0;
  ```

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

3. Clone the repository to the machine you wish to deploy to (using the latest stable tag):

    ```bash
    git clone --branch v1.0-A2 https://github.com/Alfresco/alfresco-ansible-deployment.git
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

    > NOTE: The playbook takes around 30 minutes to complete.

8. Access the system using the following URLs using a browser on the same machine:

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

* The playbook downloads several large files so you will experience some pauses while they transfer and you'll also see the message "FAILED - RETRYING: Check on war download async task (nnn retries left)." appearing many times as the WAR file downloads
* The Tomcat access log is enabled by default and will grow in size quite quickly

## Troubleshooting

The best place to start if something is not working are the log files, these can be found in the following locations:

* Nginx
  * `/var/log/alfresco/nginx.alfresco.error.log`
* Repository
  * `/var/log/alfresco/alfresco.log`
  * `/var/log/alfresco/catalina.out`
* Share
  * `/var/log/alfresco/share.log`
