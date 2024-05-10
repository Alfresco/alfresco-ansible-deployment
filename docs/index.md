---
title: Home
layout: home
nav_order: 1
---

# Alfresco Ansible Deployment

This project provides an [Ansible](https://www.ansible.com) playbook capable of
deploying Alfresco Content Services (ACS).

Ansible is an open-source software provisioning, configuration management and
application-deployment tool enabling infrastructure as code.

A user runs a playbook that deploys to any number of hosts as shown in the
diagram below.

![Ansible Overview](./resources/ansible-overview.png)

## Prerequisites

* If you want to install the Enterprise version, Nexus credentials for [https://artifacts.alfresco.com](https://artifacts.alfresco.com) are required.

## Documentation

Please start from the [Overview](overview.md) if you are getting started
for the first time with this project and the playbook or go directly to the
[deployment guide](deployment-guide.md) to learn how to run the playbook.

Users upgrading from previous versions of the playbook may want to take a look
to [Upgrade Notes](playbook-upgrade.md).

## Development

Developer's guide is available on the
[GitHub Repository](https://github.com/Alfresco/alfresco-ansible-deployment?tab=readme-ov-file#alfresco-ansible-deployment).

## License

The code in this repository is released under the Apache License, see the
[LICENSE](https://github.com/Alfresco/alfresco-ansible-deployment/blob/master/LICENSE) file for details.
