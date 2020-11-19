# Documentation

Ansible models your IT infrastructure by describing how all of your systems inter-relate, rather than just managing one system at a time.

It uses no agents and no additional custom security infrastructure, so it's easy to deploy - and most importantly, it uses a very simple language (YAML, in the form of Ansible Playbooks) that allow you to describe your automation jobs in a way that approaches plain English.

Source: https://www.ansible.com/overview/how-ansible-works

The diagram below shows how the ACS playbook uses the roles when deploying onto a single machine.

![Single Machine Deployment](./resources/acs-single-machine.png)

The diagram below shows how the ACS playbook uses the roles when the deployment is spread across multiple machines.

![Multi Machine Deployment](./resources/acs-multi-machine.png)

At this point it's unclear whether there will be a playbook to deploy a fully highly available system. The diagram below shows what this might look like if we were to implement this.

![High Availability Deployment](./resources/acs-ha.png)



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

