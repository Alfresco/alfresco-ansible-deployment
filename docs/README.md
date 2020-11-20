# Documentation

Ansible models your IT infrastructure by describing how all of your systems inter-relate, rather than just managing one system at a time.

It uses no agents and no additional custom security infrastructure, so it's easy to deploy - and most importantly, it uses a very simple language (YAML, in the form of Ansible Playbooks) that allow you to describe your automation jobs in a way that approaches plain English.


>Source: https://www.ansible.com/overview/how-ansible-works

**Quick overview of the project structure.**

The project contains a playbook and multiple roles.

An Ansible playbook is a file where users write Ansible code, an organized collection of scripts defining the work of a server configuration. 

ACS playbook can be found in the _playbooks_ directory. Because the project makes use of ansible role structure, the playbook contains only definitions of the roles, and all the logic is perfomed by them, thus making the project both granular and easy to maintain.

Ansible role is an independent component which allows reuse of common configuration steps. Ansible role is a set of tasks to configure a host to serve a certain purpose like configuring a service. Roles are defined using YAML files with a predefined directory structure.
A role directory structure contains directories: defaults, vars, tasks, files, templates, meta, handlers. 

**defaults**: contains default variables for the role. Variables in default have the lowest priority so they are easy to override.  
**vars**: contains variables for the role. Variables in vars have higher priority than variables indefaults directory.  
**tasks**: contains the main list of steps to be executed by the role.  
**files**: contains files which we want to be copied to the remote host. We don’t need to specify a path of resources stored in this directory.  
**templates**: contains file template which supports modifications from the role. We use the Jinja2 templating language for creating templates.  
**meta**: contains metadata of role like an author, support platforms, dependencies.  
**handlers**: contains handlers which can be invoked by “notify” directives and are associated withservice.

Roles or services deployed by the acs playbook:

* **activemq** - deploys Apache ActiveMQ on the specified host
* **adw** - deploys Alfresco Digital Workspace
* **common** - contains a set of common tasks that prepares the specified host for other roles (creates user and group, common directories)
* **java** - contains a set of tasks that installs OpenJDK on the specified host 
* **nginx** - contains a set of tasks that installs NGINX on the specified host
* **postgres** - contains a set of tasks that installs PostgreSQL on the specified host
* **repository** - deploys Alfresco Repository and Alfresco Share on the specified host
* **search** - deploys Alfresco Search Services on the specified host
* **sfs** - deploys Alfresco Shared File Store on the specified host
* **sync** - deploys Alfresco Sync Services on the specified host
* **tomcat** - deploys Apache Tomcat on the specified host
* **transformers** - deploys Alfresco Transform Service on the specified host
* **trouter** - deploys Alfresco Transform Router on the specified host

The diagram below shows how the ACS playbook uses the roles when deploying onto a single machine.

![Single Machine Deployment](./resources/acs-single-machine.png)

The diagram below shows how the ACS playbook uses the roles when the deployment is spread across multiple machines.

![Multi Machine Deployment](./resources/acs-multi-machine.png)

At this point it's unclear whether there will be a playbook to deploy a fully highly available system. The diagram below shows what this might look like if we were to implement this.



The components and their respective versions that are deployed by this ansible playbook.

| Component | Version |
|-----------|---------|
| alfresco.war | 6.2.2 |
| share.war | 6.2.2 |
| ROOT.war  | 6.0.1 |
| api-explorer.war | 6.3.0 |
| _vti_bin.war.war | 1.3.1 |
| alfresco-aos-module.amp | 1.3.1 |
| alfresco-device-sync-repo.amp | 3.3.3.1 |
| alfresco-googledrive-share.amp | 3.2.0 |
| alfresco-googledrive-repo-enterprise.amp | 3.2.0 |
| alfresco-digital-workspace | 1.6.0 |
| alfresco-search-services | 1.4.2 |
| alfresco-transform-core-aio-boot | 2.3.5 |
| alfresco-shared-file-store-controller | 0.8.0 |
| alfresco-transform-router | 1.3.1 |
| Apache ActiveMQ | 5.15.13 |
| OpenJDK | 11.0.7 |
| Apache Tomcat | 8.5.56 |
| PostgreSQL | 11 |
