# Upgrading an environment

The ACS installation is made of several components among which:

- Content service
- share
- digital workspace
- Search service
- ...

## Pre-requisites

Before proceeding to an upgrade, an administrator needs to:

- Make sure the [upgrade path and documentation](https://docs.alfresco.com/content-services/latest/upgrade/) is followed
- Appropriate backups of database, contentstore and indexes are done and can be restored in case a rollback is needed
- Initial deployment must have been done using this Ansible playbook

## Supported Components

Below is a description of the supported upgrade procedure for each supported component (at the time of writing it's only hotfix upgrades for ACS repository)

### Content service (repository)

#### Upgrade types

There are different kinds of upgrade one may want to proceed. For example a major upgrade would be upgrading from 7.0.x to 7.1.x.
A minor upgrade (or service pack upgrade) would be moving from 7.0.0 to 7.0.1.
Both major and minor upgrades require setting up a new environment and porting data and customizations from the source environment to the target one. The main reason behind this limitation is that major upgrades usually come with underlying software stack changes.
These migrations cannot be done "in-place".

Alfresco also releases some hotfixes and an hotfix upgrade would be moving from 7.0.1 to 7.0.1.4. This type of upgrade can be done "in-place" and is supported by the playbook.

> Please note that "in-place" upgrade still need to match the upgrade pre-requisites

#### Proceeding to a hotfix "in-place" upgrade

In order to apply a later hotfix, you need to first match the pre-requisites, then change the ACS version to point to the hotfix version in the appropriate file, and finally run the playbook again.

In the example bellow we want to upgrade from the initial 7.0.1 installation to 7.0.1.4 hotfix:

Edit `7.0.N-extra-vars.yml` and changes the the bellow snippet:

```yaml
acs:
  repository: "{{ nexus_repository.enterprise_releases }}/alfresco-content-services-distribution"
  version: 7.0.1
  edition: Enterprise
```

to:

```yaml
acs:
  repository: "{{ nexus_repository.enterprise_releases }}/alfresco-content-services-distribution"
  version: 7.0.1.4
  edition: Enterprise
```

> IMPORTANT: make sure you do not set the version to a version number that's not a hotfix (version number needs to be 4 digits and the 3 first ones needs to match the ones of the initially deployed version)
> This is because, as explained earlier, "in-place" upgrades are only supported for hotfixes

Once these changes are saved run the command bellow:

```bash
ansible-playbook playbooks/acs.yml -i inventory_ssh.yml -e "@7.0.N-extra-vars.yml"
```

> Note: Use whatever inventory and config file that matches your use case
> If you're applying a hotfix to the latest major release (7.1 as of writing) you don't need to specify an extra config file with "-e @file"

After the playbook ran successfully your environment delivers the upgraded version of repo but the previous installation is still on the target machine. It is the admin responsibility to make sure the new system works as expected and no rollback is needed. If all is OK, the old installation previous installation can be cleaned by removing the folder: `{{ binaries_folder }}/content-services-{{ acs.version }}` (by default points to: `/opt/alfresco/content-services-7.0.1`).

#### Rolling back a hotfix "in-place" upgrade

If something goes wrong with the upgrade, or if tests are not successful after upgrade completed, rolling back the environment can be done by following the steps bellow:

- restoring Database and contentstore backup
- reverting the version changes to previous state in the config file (either `group_vars/all` or version specific config files)
- running the playbook again.

## Upgrade impacts

### Hotfix "in-place" upgrades

This process will restart tomcat on all the repository nodes and there is no guarantee one node is stopped only after the others have restarted. As a consequence a short service outage needs to be scheduled
