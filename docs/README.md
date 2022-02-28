# Documentation

This page provides an overview of Ansible, the project structure and the components deployed.

## Ansible Overview

[Ansible](https://www.ansible.com/overview/how-ansible-works) models your IT infrastructure by describing how all of your systems inter-relate, rather than just managing one system at a time.

It doesn't use any agents nor additional custom security infrastructure, so it's easy to deploy - and most importantly, it uses a very simple language, YAML, in the form of Ansible Playbooks that allow you to describe your automation jobs in a way that approaches plain English.

An Ansible playbook contains one or more roles. A role is an independent component which allows reuse of common configuration steps. It consists of a set of tasks used to configure a host to serve a certain purpose, for example, configuring a service. This is depicted in the diagram below.

![Playbook Ovewview](./resources/playbook-overview.png)

Roles are defined using YAML files with a predefined directory structure.

A role directory structure contains directories: defaults, vars, tasks, files, templates, meta, and handlers.

* **defaults** contains default variables for the role. Variables in defaults have the lowest priority so they are easy to override
* **vars** contains variables for the role. Variables in vars have higher priority than variables in the defaults directory
* **tasks** contains the main list of steps to be executed by the role
* **files** contains files which we want to be copied to the remote host. We don’t need to specify a path of resources stored in this directory
* **templates** contains file templates which support modifications from the role. We use the Jinja2 templating language for creating templates
* **meta** contains metadata of the role like an author, support platforms, and dependencies
* **handlers** contains handlers which can be invoked by “notify” directives and are associated with a service

## Project Overview

The project contains a playbook and multiple roles.

The ACS playbook can be found in the _playbooks_ directory. Because the project makes use of ansible role structure, the playbook contains only definitions of the roles, and all the logic is perfomed by them, thus making the project both granular and easy to maintain.

The playbook uses the following roles:

* **activemq** - deploys and configures Apache ActiveMQ
* **adw** - deploys and configures Alfresco Digital Workspace
* **common** - contains a set of common tasks that prepares the specified host for other roles (creates user and group, common directories)
* **java** - deploys OpenJDK
* **nginx** - deploys and configures Nginx as a proxy
* **postgres** - deploys and configures PostgreSQL
* **repository** - deploys and configures Alfresco Repository and Alfresco Share
* **search** - deploys and configures Alfresco Search Services
* **sfs** - deploys and configures Alfresco Shared File Store
* **sync** - deploys and configures Alfresco Sync Service
* **tomcat** - deploys and configures Apache Tomcat
* **transformers** - deploys and configures Alfresco Transform Service
* **trouter** - deploys and configures the Transform Router

The same playbook can be run to deploy the system in several different ways, please refer to the [deployment guide](./deployment-guide.md) for a step by step set of instructions.

## Versioning

While ACS supports a wide range of OS, the playbook is only known to work and is supported for a subset of them. The table below gives detailed information on the status of supported OS (which we aim at growing with time).

| OS Flavor / version | 7.0 Enterprise | 6.2.2 Enterprise | Community |
|-|-|-|-|
| Amazon Linux (v2) | :x: | :x: | :x: |
| Amazon Linux (v1) | :x: | :x: | :x: |
| RHEL 8.2 | :heavy_check_mark: | - | :heavy_check_mark: |
| RHEL 7.7 | :heavy_check_mark: | - | :heavy_check_mark: |
| RHEL 7.6 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CentOS 8 x64 | :heavy_check_mark: | - | :heavy_check_mark: |
| CentOS 7 x64 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Ubuntu 20.04 | :heavy_check_mark: | - | :heavy_check_mark: |
| Ubuntu 18.04 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SUSE 15.0 | :x: | - | :x: |
| SUSE 12.0 SP1 x64 | :x: | :x: | :x: |

> Ansible version 2.12.x is used for testing this playbook

The table below shows the version of the components deployed by the playbook for ACS 7.x and 6.2.N.

| Component | 7.1 Enterprise | 7.0.N Enterprise | 6.2.N Enterprise | Community |
|-|-|-|-|-|
| OpenJDK | 11.0.13 | 11.0.13 | 11.0.13 | 11.0.13 |
| Apache Tomcat | 9.0.54 | 9.0.54 | 8.5.72 | 9.0.54 |
| PostgreSQL | 13.x | 13.x | 11.x | 13.x |
| Apache ActiveMQ | 5.16.1 | 5.16.1 | 5.15.14 | 5.16.1 |
| Repository | 7.1.1 | 7.0.1.4 | 6.2.2 | 7.1.1.2 |
| Share | 7.1.1 | 7.0.1.4 | 6.2.2 | 7.1.1.2 |
| Search Services | 2.0.2 | 2.0.1.1 | 1.4.3 | 2.0.2 |
| All-In-One Transformation Engine | 2.5.6 | 2.3.10 | 2.5.6 | 2.5.6 |
| AOS | 1.4.0 | 1.4.0 | 1.3.1 |  |
| GoogleDocs | 3.2.1 | 3.2.1 | 3.2.0 |  |
| Digital Workspace | 2.6.0 | 2.1.0 | 2.6.0 | N/A |
| Transform Router | 1.5.1 | 1.3.2 | 1.5.1 | N/A |
| Shared File Store | 0.16.1 | 0.13.0 | 0.16.1 | N/A |
| Sync Service | 3.5.0 | 3.4.0 | 3.3.3.1 | N/A |
