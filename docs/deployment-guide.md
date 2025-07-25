---
title: Deployment guide
nav_order: 3
---

# Deployment guide

This page describes how to deploy Alfresco Content Services (ACS) using the Ansible playbook found in this project.

A basic understanding of Ansible concepts is highly recommended to successfully
complete the deployment and better understand all the steps documented in this
guide. If it's your first time with Ansible, please have a read at [Ansible
concepts](https://docs.ansible.com/ansible/latest/user_guide/basic_concepts.html)
for a brief introduction.

* [Deployment guide](#deployment-guide)
  * [Getting started quickly with Vagrant](#getting-started-quickly-with-vagrant)
  * [Getting started](#getting-started)
    * [Get the playbook](#get-the-playbook)
    * [Setup Python runtime](#setup-python-runtime)
      * [Additional requirements for Python 3.12+ on Ubuntu/Debian](#additional-requirements-for-python-312-on-ubuntudebian)
    * [Install ansible dependencies via pipenv](#install-ansible-dependencies-via-pipenv)
  * [Minimal configuration](#minimal-configuration)
  * [Understanding the playbook](#understanding-the-playbook)
    * [The Control Node](#the-control-node)
    * [Understanding the inventory file](#understanding-the-inventory-file)
    * [Folder Structure](#folder-structure)
    * [Service Configuration](#service-configuration)
    * [TCP Port Configuration](#tcp-port-configuration)
  * [Configure Your Deployment](#configure-your-deployment)
    * [License](#license)
    * [Secrets management](#secrets-management)
      * [Enable Ansible Vault support](#enable-ansible-vault-support)
      * [Populate secrets with Ansible Vault](#populate-secrets-with-ansible-vault)
        * [Encrypted variables](#encrypted-variables)
        * [Encrypted files](#encrypted-files)
      * [Third-party lookup plugins](#third-party-lookup-plugins)
    * [Alfresco Global Properties](#alfresco-global-properties)
    * [Enable SSL](#enable-ssl)
    * [AMPs](#amps)
    * [JVM Options](#jvm-options)
    * [Single Sign On (Keycloak)](#single-sign-on-keycloak)
      * [SSO known issues and limitations](#sso-known-issues-and-limitations)
    * [External Databases](#external-databases)
    * [External ActiveMQ](#external-activemq)
    * [External ElasticSearch](#external-elasticsearch)
    * [External Identity](#external-identity)
    * [Custom Keystore](#custom-keystore)
    * [Specifying a different component repository](#specifying-a-different-component-repository)
  * [Localhost Deployment](#localhost-deployment)
  * [SSH Deployment](#ssh-deployment)
    * [Single Machine Deployment](#single-machine-deployment)
    * [Multi Machine Deployment](#multi-machine-deployment)
    * [Additional command switches for ansible-playbook](#additional-command-switches-for-ansible-playbook)
  * [ACS cluster](#acs-cluster)
  * [Maintenance](#maintenance)
    * [Search Enterprise Reindexing](#search-enterprise-reindexing)
  * [Cleanup and uninstall ACS](#cleanup-and-uninstall-acs)
    * [Cleanup](#cleanup)
    * [Uninstallation](#uninstallation)
  * [Known Issues](#known-issues)
  * [Troubleshooting](#troubleshooting)
    * [Failed Downloads](#failed-downloads)
    * [Nginx Failure](#nginx-failure)
    * [Communication Failures](#communication-failures)
    * [Playbook Failures](#playbook-failures)
    * [Alfresco Failures](#alfresco-failures)

## Getting started quickly with Vagrant

The quickest way to get started and experiment with the playbook is by
leveraging Vagrant to create a Virtualbox virtual machine to act as the control
node **and** the target host.

1. Ensure your local machine has a minimum of 10G of memory and 4 CPUs
2. Clone via Git or Download this repository to your local machine
3. Install [Vagrant](https://www.vagrantup.com/downloads)
4. Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
5. Open Virtualbox application to make sure it startup correctly
6. In a terminal, navigate to where you cloned or unpacked the repository
7. Set environment variables to hold your Nexus credentials as shown below
   (replacing the values appropriately):

    ```bash
    export NEXUS_USERNAME="<your-username>"
    export NEXUS_PASSWORD="<your-password>"
    ```

8. Run the main vagrant command (you can pass any of the version currently
   supported as `VAGRANT_ACS_MAJOR_VERSION`):

    ```bash
    VAGRANT_ACS_MAJOR_VERSION=23 vagrant up
    ```

    > NOTE: The playbook takes around 30 minutes to complete and mostly depends
    > on your internet connection speed.

If any step fails, you can re-run the provisioning step with:

```bash
vagrant provision
```

If you want to start from scratch, you can destroy the VM and start again with:

```bash
vagrant destroy
vagrant up
```

Once ACS has initialized access the system using the following URLs using a browser:

* Digital Workspace: `http://localhost/workspace`
* Share: `http://localhost/share`
* Repository: `http://localhost/alfresco`
* API Explorer: `http://localhost/api-explorer`

To access the machine vagrant created and ran the playbook on use `vagrant ssh`.

## Getting started

If you have access to a pristine host running one of the supported Linux
distributions, you can follow this quickstart for a localhost deployment.

### Get the playbook

If you're not working directly working on the control node, transfer the ZIP
file to the control node together with the SSH private key required to login to
the target machines, and SSH into the machine:

```bash
scp  alfresco-ansible-deployment-<version>.zip user@controlnode:
ssh-copy-id -i ~/.ssh/ansible_rsa user@controlnode
ssh  user@controlnode
unzip alfresco-ansible-deployment-<version>.zip
cd alfresco-ansible-deployment
```

You can also use Git to fetch latest sources (or a specific release for example
by adding `-b v2.4.0`) on the control node with:

```bash
git clone https://github.com/Alfresco/alfresco-ansible-deployment.git
cd alfresco-ansible-deployment
```

> You may want to generate an SSH key pair locally and use it later for
> deployment. Wether you generate one or you use one you copied over to the
> control node, it is your responsibility to deploy it to the target machines so
> Ansible can use it. Using SSH keys is recommended but not mandatory. If using
> password instead make sure to add the `-k`switch to the ansible command so it
> prompts you for a password.

### Setup Python runtime

Before starting using the playbook, make sure you are running at least Python 3.11:

```bash
python3 --version
```

If not, depending on your distribution, you may need to install Python 3.11. For
example, on Ubuntu 22.04 you can install it with:

```bash
sudo apt-get install python3.11 python3-pip
```

and on rpm-based distributions like Rocky Linux and Red Hat:

```bash
sudo dnf install python3.11-pip
```

Then check again the version with:

```bash
python3.11 --version
```

We made mandatory the usage of [pipenv](https://pipenv.pypa.io/en/latest/) to
make sure that you will run the playbook with the same set of python
dependencies we are running our integration tests.

Install pipenv via pip (alternate [install methods](https://pipenv.pypa.io/en/latest/installation.html)):

```bash
pip3 install --user pipenv
```

> Try with `python3.11 -m pip` instead of `pip3` if there is more than one
> python version in your system and 3.11 is not the default one.

#### Additional requirements for Python 3.12+ on Ubuntu/Debian

If you are using an operating system with Python 3.12 or higher on a
Debian derivative (e.g. Ubuntu 24.04), there is a breaking change which will
prevent you from installing pipenv using the `pip` install command above.

The most easy way to workaround this is to install pipenv using the
binary package:

```bash
sudo apt-get install pipenv
```

Another more generic way (which works on any OS) is to install pipenv inside a
virtual environment (venv) as described below.

Create a new venv within the repository root folder with:

```bash
python3.12 -m venv venv
```

Then activate the venv with:

```bash
source venv/bin/activate
```

Finally, install pipenv in the venv with:

```bash
pip3 install pipenv
```

### Install ansible dependencies via pipenv

Now you are ready to install Ansible and required runtime dependencies in a dedicated
virtual environment managed by pipenv.

Run from the repository root folder:

```bash
pipenv install --deploy
pipenv run ansible-galaxy install -r requirements.yml
```

> When using `pipenv`, it is sufficient to prefix any ansible command with
> `pipenv run`. We always provide command snippets in this documentation with
> that prefix for your copy-pasting convenience. Keep in mind that you can also
> run `pipenv shell` that will spawn a new shell that automatically assume that
> every command is related to the current pipenv virtualenv. You can exit from
> that shell just by using `exit` or `Ctrl+D`.

If you intend to deploy an Enterprise system, create the mandatory environment
variables that hold your Nexus credentials as shown below (replacing the values
appropriately):

```bash
export NEXUS_USERNAME="<your-username>"
export NEXUS_PASSWORD="<your-password>"
```

Now you have the control node setup you can
[configure](#configure-your-deployment) your deployment and decide what kind of
deployment you would like.

To deploy everything on the control node follow the steps in the [Localhost
Deployment](#localhost-deployment) section or to deploy to one or more other
machines follow the steps in the [SSH Deployment](#ssh-deployment) section.

If you are going to do a production deployment, please take a look at the
mandatory [Secrets management](#secrets-management) section.

Alternatively, you can add the parameter `-e autogen_unsecure_secrets=true` to
the `ansible-playbook` command to just autogenerate secrets before running the
playbook for the first time (remove it for the next runs).

## Minimal configuration

In order to run the playbook successfully you least to provide *AT LEAST* the
domain name where the Alfresco applications will be served. The `acs_play_known_urls` is
used for that purpose.  It should contain any URL which is allowed to query the
repository and the first entry MUST be set to the domain URL used to access
Alfresco. For example if you plan on using ecm.acme.com as your main domain on
both https & http, you should set the `playbooks/group_vars/all.yml` file to:

```yaml
acs_play_known_urls:
  - https://ecm.acme.com/share
  - http://ecm.acme.com/share
```

> The `acs_play_known_urls` variable serves a larger purpose, check the
> [SECURITY README](SECURITY.md) for more details.

## Understanding the playbook

Let's take a step back to learn more about Ansible and the playbook before
moving to more advanced topics.

### The Control Node

The machine the playbook is run from is known as the Control Node. Ansible has
some prerequisites for this control node. The main one is that it needs to run
on a POSIX compliant system, meaning Linux or others Unix (including MacOSX)
but not Windows.
On windows please make see the provided `Vagrantfile` in order to kick start a
local Linux VM where to deploy the playbook.

More info on [control
node](https://docs.ansible.com/ansible/latest/user_guide/basic_concepts.html#control-node)

### Understanding the inventory file

An inventory file is used to describe the architecture or environment where you
want to deploy the ACS platform. Each machine taking part in the environment
needs to be described with at least:

* An `inventory_name`: a name which, in most cases can be anything (It is
  though a good practice to use a name or address which all target machines can
  resolve and reach from their local network).

And optionally:

* An `ansible_user` variable: if the host requires a unique and specific user
  to login to.
* An `ansible_host` variable; if the host needs to be reached through an
  address that's different from the `inventory_hostname` (e.g. machine is only
  reachable through a bastion host or some sort of NAT).
* An `ansible_private_key_file` in case your hosts needs a specific SSH key in
  order to login to it.

An ACS inventory file has the following groups a host can belong to:

* `repository`: the list of one or more hosts which will get an Alfresco repo
  deployed on (see [the deployment guide](#acs-cluster) for details on
  repository clustering).

* `database`: a host on which the playbook will deploy PostgreSQL. See the
  [deployment guide](./deployment-guide.md) for details on how to use another
  external RDBMS.
* `activemq`: the host on which the playbook will deploy the message queue
  component required by ACS.
* `external_activemq`: an alternative group to `activemq` in case you don't want
  to deploy ActiveMQ using our basic activemq role but instead use an ActiveMQ
  instance of yours which matches your hosting standards.
* `search`: a single host on which to deploy Alfresco Search services, as an
  alternative to Search Enterprise.
* `search_enterprise`: one or more hosts on which deploy Search Enterprise.
* `elasticsearch`: one or more hosts on which deploy the ElasticSearch cluster
  backing Search Enterprise.
* `external_elasticsearch`: an alternative group to `elasticsearch` in case you
  don't want to deploy ElasticSearch using the [community ElasticSearch
  role](https://github.com/geerlingguy/ansible-role-elasticsearch) but instead
  use an ElasticSearch cluster of yours which matches your hosting standards.
* `nginx`: a single host on which the playbook will deploy an NGINX reverse
  proxy configured for the numerous http based service in the platform.
* `acc`: a single host where you want the Alfresco Control Center UI to be installed
* `adw`: a single host where you want the Alfresco Digital Workspace UI to be installed
* `transformers`: a single host where the playbook will deploy the Alfresco
  Transformation Services components
* `syncservice`: a single host where the Alfresco Device Sync service will be deployed
* `identity`: a single host where the playbook will deploy Keycloak with local storage
* `external_identity`: an alternative group to `identity` in case you want to
  provide your already existing keycloak installation (not yet implemented)

> Ansible also ships a default group called `all` which all hosts always
> belongs to

Inventory files provided as example in this playbook are all YAML written.
Groups are always children items of the `all` group it self or of other groups.
Hosts are mentioned after a `hosts` key under any group (including the `all`
group). So a generic example would be:

```yaml
---
all:
  children:
    group_name1:
      hosts:
        inventory_nameA:
```

An inventory file can also be used to set variable within a specific scope.
Variables can be specified at the host, groups or all levels, thus affecting
the scope in which that variable is available.
So if one variable (like `ansible_user` for example) is valid for all hosts,
you'd better set it once under the `all` group.

See [Ansible variable precedence
documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#understanding-variable-precedence)
to better understand how precedence works.

In most cases we recommend you use your inventory to place the configuration
variables you may need to tweak the playbook to your needs.

In this project you'll find 3 example inventory files:

The `inventory_local.yml` which is ready to use in order to deploy all
components on the local machine.

```mermaid
flowchart LR
user[👤] --> Playbooks
subgraph Control Node
  Playbooks
  Inventory
  role1[[role1]]
  roleN[[roleN]]
end
Playbooks --- Inventory
Playbooks --> role1
Playbooks --> roleN
```

The `inventory_ssh.yml` which provides s skeleton for you to update and match
your architecture so each component can be deployed on a dedicated node.

```mermaid
flowchart LR
user[👤] --> Playbooks
subgraph Control Node
  Playbooks
  Inventory
end
subgraph node1
  role1[[role1]]
end
subgraph nodeN
  roleN[[roleN]]
end
Playbooks --> node1
Playbooks --> nodeN
Inventory --- Playbooks
```

The `inventory_ha.yml` which is very similar to the previous one but also
provides support for repository clustering (see [acs cluster section](#acs-cluster) for more details).

A complete documentation about inventory file is available at [inventory file](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#intro-inventory)

### Folder Structure

Regardless of role and connection type, a consistent folder structure is used.
You will find the deployed files in the following locations:

| Path                | Purpose       |
|:--------------------|:--------------|
| `/opt/alfresco`     | Binaries      |
| `/etc/opt/alfresco` | Configuration |
| `/var/opt/alfresco` | Data          |
| `/var/log/alfresco` | Logs          |

### Service Configuration

The following systemd services are deployed and can be used to stop and start Alfresco components:

| Service Name                              | Purpose                                                                                 |
|:------------------------------------------|:----------------------------------------------------------------------------------------|
| `activemq.service`                        | ActiveMQ Service                                                                        |
| `postgresql-<version>.service`            | Postgresql DB Service (where `<version>` is 15 for ACS 23 and 14 for 7.4 and 7.3)       |
| `nginx.service`                           | Nginx Service                                                                           |
| `alfresco-content.service`                | Alfresco Content Service                                                                |
| `alfresco-search.service`                 | Alfresco Search Service                                                                 |
| `alfresco-shared-fs.service`              | Alfresco Shared File Store Controller Service                                           |
| `alfresco-sync.service`                   | Alfresco Sync Service                                                                   |
| `alfresco-tengine-aio.service`            | Alfresco AIO Transform Core Engine                                                      |
| `alfresco-transform-router.service`       | Alfresco Transformation Router Service                                                  |
| `elasticsearch-connector.service`         | Alfresco Search Enterprise Service                                                      |
| `elasticsearch-connector-reindex.service` | Alfresco Search Enterprise job to force the reindexing of all the contents of the store |
| `elasticsearch.service`                   | ElasticSearch Service                                                                   |
| `keycloak.service`                        | Keycloak Service                                                                        |
| `alfresco-audit-storage.service`          | Alfresco Audit Storage service                                                          |

Please be aware that some configuration changes (e.g. postgres pg_hba,
properties files, ...) can trigger a service restart and a consequent
application downtime. For this reason you may want to run the playbook only
during a scheduled maintenance window.

### TCP Port Configuration

Several roles setup services that listen on TCP ports and several roles wait
for TCP ports to be listening before continuing execution (indicated by `Yes`
in the "Required For Deployment" column). The table below shows the
communication paths and port numbers used.

| Target Host                 | Target Port | Source Hosts                                             | Required For Deployment |
|:----------------------------|:------------|:---------------------------------------------------------|:------------------------|
| activemq                    | 61616       | repository, syncservice, transformers, search_enterprise | Yes                     |
| database                    | 5432        | repository, syncservice, search_enterprise (reindex)     | Yes                     |
| database                    | 5432        | search_enterprise (reindex)                              | No                      |
| repository                  | 8080        | nginx, share (loopback only)                             | Yes                     |
| repository                  | 80          | search, syncservice                                      | Yes                     |
| search                      | 8983        | repository                                               | No                      |
| transformers (aio t-engine) | 8090        | repository                                               | No                      |
| transformers (router)       | 8095        | repository                                               | No                      |
| transformers (sfs)          | 8099        | repository                                               | No                      |
| syncservice                 | 9090        | nginx                                                    | No                      |
| acc                         | 8881        | nginx                                                    | No                      |
| adw                         | 8880        | nginx                                                    | No                      |
| nginx                       | 80,443      | `<client-ips>` (e.g. api clients such as acc or adw)     | No                      |
| elasticsearch               | 9200        | repository                                               | No                      |
| keycloak                    | 8082        | nginx                                                    | No                      |
| keycloak                    | 443         | repository                                               | No                      |

> NOTE: When using the ACS Community, some of these ports do not need to be opened (e.g. transform router/sfs, acc, adw).

## Configure Your Deployment

By default, without any configuration applied, the playbook will deploy a
limited trial of the Enterprise version of Alfresco Content Services that
goes into read-only mode after 2 days.

The sections below describe how you can configure your deployment before running the playbook.

### License

If you have a valid license place your `.lic` file in the `configuration_files/licenses` folder before running the playbook.

> NOTE: You can also [upload a license][upload-license] via the Admin Console once the system is running.

### Secrets management

This playbook expects that security-relevant secrets are configured within the
`vars/secrets.yml` file.

It is strongly recommended to enable [Ansible
Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) encryption
or use [third-party plugins](#third-party-lookup-plugins) to avoid keeping
secrets in plaintext on the control node file-system.

We provide a `secrets-init.yml` playbook to automatically generate secure
secrets and encrypt them with Ansible Vault.

#### Enable Ansible Vault support

To start using **Ansible Vault** integration, a password needs to be provided to
Ansible to make encryption/decryption working during the play.

There are different ways to provide that password Ansible Vault, from manually
via user input on each ansible-playbook run using the `--ask-vault-pass` flag
(example below), to more advanced scenarios.

```bash
pipenv run ansible-playbook --ask-vault-pass playbooks/acs.yml
```

While we recommend to refer to the official Ansible documentation to properly configure
[Ansible vault](https://docs.ansible.com/ansible/latest/vault_guide/vault_managing_passwords.html),
below a basic configuration that will help you in quickly installing Alfresco
without to having to input the Vault password every time.

Configure a password in a file (e.g. `~/.vault_pass.txt`), optionally
autogenerate it with:

```bash
openssl rand -base64 21 > ~/.vault_pass.txt
```

Set `ANSIBLE_VAULT_PASSWORD_FILE` to that file location so that can
automatically picked-up when running Ansible:

```bash
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt
```

Now you are ready to start using Ansible Vault.

#### Populate secrets with Ansible Vault

Ansible Vault provides two alternative ways to protect secrets:

* [Encrypted variables](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#encrypting-individual-variables-with-ansible-vault)
* [Encrypted files](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#encrypting-files-with-ansible-vault)

In the previous links you can read both advantages and disadvantages of the two approaches.

> If you are upgrading from previous versions of the playbook, you may want to
> read [upgrade notes](playbook-upgrade.md#secrets-management).

##### Encrypted variables

With Encrypted variables you can use the `secrets-init.yml` playbook to
handle the first-time generation of secrets and also to automatically add new
secrets that may be introduced in future versions of the playbook.

To automatically setup/update secrets, run:

```bash
pipenv run ansible-playbook -e vault_init=encrypted_variables playbooks/secrets-init.yml
```

##### Encrypted files

With Encrypted files you can use the `secrets-init.yml` playbook to handle
the first-time generation of secrets but for updates you have to provide them as
described below. However you can provide your own passwords too.

```bash
pipenv run ansible-playbook -e vault_init=plaintext playbooks/secrets-init.yml
```

and then replace the autogenerated passwords with your own.

To enable file encryption and automatically autogenerate any missing secrets,
run:

```bash
pipenv run ansible-playbook  -e vault_init=encrypted_file playbooks/secrets-init.yml
```

After the first run, you can access the encrypted file vault with:

```bash
pipenv run ansible-vault view vars/secrets.yml
```

or to add/edit secrets with:

```bash
pipenv run ansible-vault edit vars/secrets.yml
```

Please refer to the [official documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html) to learn how to interact with existing encrypted variables or files.

#### Third-party lookup plugins

Variables defined in `vars/secrets.yml` can also reference remote values using
third-parties lookup plugins instead of using Ansible Vault.

To generate a stub secrets file, run:

```bash
pipenv run ansible-playbook -e vault_init=plugin playbooks/secrets-init.yml
```

And then edit `vars/secrets.yml` to fill all the required arguments for the plugin you want to use as described in the plugin documentation pages:

* [HashiCorp Vault](https://docs.ansible.com/ansible/latest/collections/community/hashi_vault/hashi_vault_lookup.html)
* [AWS Secrets](https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_secret_lookup.html)
* [1Password](https://docs.ansible.com/ansible/latest/collections/community/general/onepassword_lookup.html)
* [CyberArk](https://docs.ansible.com/ansible/latest/collections/community/general/cyberarkpassword_lookup.html)

### Alfresco Global Properties

You can provide your [repository configuration][global-properties] by editing
the `configuration_files/alfresco-global.properties` file.

> This approach is now discouraged and you should prefer using the [`repository`
> group vars](https://github.com/Alfresco/alfresco-ansible-deployment/blob/master/configuration_files/alfresco-global.properties)
> `global_properties` as much as possible otherwise reference you own snippets
> of properties file using either the new `repository` group var
> `properties_snippets` or directly the `repository` role argument
> `repository_raw_properties`.

`alfresco-global.properties` will be located in
`/etc/opt/alfresco/content-services/classpath`.

### Enable SSL

If you want to deploy the Alfresco platform with your own SSL certificate, place
the certificate and key in the `configuration_files/ssl_certificates` folder
before running the playbook.

Ensure that the domain associated with this certificate is listed first in
`acs_play_known_urls`. Additionally, update `playbooks/group_vars/all.yml` by
setting:

* `acs_play_fqdn_alfresco` to your domain (e.g., `your_domain.com`).
* `acs_play_use_ssl: true` to enable SSL.

> NOTE: The certificate and the key should be named the same as the domain eg:
> `your_domain.com.key` and `your_domain.com.crt`

### AMPs

During playbook execution, multiple AMP files are downloaded and applied. These
files are defined as variables with the `acs_play_repository_amp_*` prefix within
`playbooks/group_vars/repository.yml` and in version-specific files located in
`vars/acsXX.yml`.

Additionally, variables prefixed with `acs_play_community_repository_amp_*` are
used when deploying the community version of ACS.

At runtime, the list of AMP files is dynamically determined while executing the
`acs.yml` playbook. The final list is stored in the
`acs_play_repository_amp_downloads` variable.

To add a custom AMP file, use the `acs_play_repository_extra_amp_downloads`
variable in `playbooks/group_vars/repository.yml`. Follow the structure provided
in the commented example below:

```yml
acs_play_repository_extra_amp_downloads: []
  # - url: "https://your.repo.com/path/to/your/artifacts/your-amp.amp"
  #   name: your-amp # optional, name is used for upgrade checks
  #   version: 1.0.0 # optional, version is used for upgrade checks
  #   checksum: "sha1:2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
  #   dest: "{{ repository_content_folder }}/<amps_repo|amps_share>/your-amp.amp"
  #   url_username: your_username_to_repo
  #   url_password: your_password_to_repo
```

> :warning: `name` and `version` are not mandatory but highly recommended to
> use, they are used in the upgrade checks to avoid unsupported upgrades.

### JVM Options

Each Java based service deployed by the playbook is configured with some default settings, including memory settings.

The defaults are defined in the roles' specific default variables (see the [Ansible Overview paragraph in the README file](./README.md)) so they can be overridden in the inventory_file using the right scope.

For example, to override the JAVA_OPTS environment variable for the All-In-One Transform Engine place the following in inventory file:

```yaml
---
all:
  children:
    transformers:
      transformers_tengine_environment:
        JAVA_OPTS:
          - -Xms512m
          - -Xmx1g
          - $JAVA_OPTS
```

All the `_environment` variables defined in roles are dictionaries, and all their keys are added to the relevant components start script thus allowing you to define any number of environment variables. Key values are a list of strings to allow for easier manipulation.
When overriding the default env vars you should make sure you're not retiring important ones so always take a look at the ``roles/ROLE_NAME/defaults/main.yml` file first.

### Single Sign On (Keycloak)

> We are providing an `identity` role as an easy way to evaluate SSO features in
> Alfresco and is not meant to be used in production (see [External
> Identity](#external-identity))

When defining a node into the `identity` group, the [identity
role](https://github.com/Alfresco/alfresco-ansible-deployment/tree/master/roles/identity)
which wraps the upstream
[ansible-middleware/keycloak][ansible-middleware/keycloak] will automatically
configure a Keycloak installation and all the components will be configured
automatically to use it (share, adw, acc).

#### SSO known issues and limitations

* The [upstream playbook][ansible-middleware/keycloak] currently supports only
* RHEL derivatives (e.g.
  Rockylinux) and not Debian based systems (internal ref: OPSEXP-2355)

[ansible-middleware/keycloak]: https://github.com/ansible-middleware/keycloak/

### External Databases

By default the playbook will deploy and configure a Postgres server for you. That server is a basic PostgreSQL setup with no specific optimization or features. For example, it doesn't provide any high availability mechanism.

> This server also requires to NOT have a sudo configuration with `requirestty` set.

If you'd prefer to use an external database server you can override the `acs_play_repo_db_url` variable.

An example custom database url is shown below:

```yaml
acs_play_repo_db_url: jdbc:mysql://54.164.117.56:3306/alfresco?useUnicode=yes&characterEncoding=UTF-8
acs_play_repo_db_driver: com.mysql.jdbc.Driver
```

Along with the url the database driver binaries need to be provided for one or both services in the `configuration_files/db_connector_repo` and/or `configuration_files/db_connector_sync` folders.

The default database username (`acs_play_repo_db_username` and/or `acs_play_sync_db_username`) and password (`repo_db_password` and/or `sync_db_password`) in the configuration file `playbooks/group_vars/all.yml` can also be overridden with your custom values.

Please refer to the [Configuring Databases][databases] documentation for more
detailed information.

### External ActiveMQ

This playbook provides support for a single host declared inside the `activemq`
group that will deploy and configure an ActiveMQ instance that is suitable for
testing/evaluation only (no failover and default credentials).

It's strongly suggested that you provide your own ActiveMQ instance by defining
in the inventory file, exactly one host as a member of the `external_activemq` group
(nested inside the `external` group) as follows:

```yaml
all:
  children:
    external_activemq:
      hosts:
        whatever.mq.eu-west-1.amazonaws.com:
          activemq_username: alfresco
          activemq_port: 61617
          activemq_transport: tcp # or ssl
    external:
      children:
        external_activemq:
```

Every hosts under the `external` group is not directly managed by the acs
playbook and is required in the inventory just for the sake of architecture description.

### External ElasticSearch

In case you want to provide your own ElasticSearch cluster (or use AWS
OpenSearch, as an example) you can define in the inventory file exactly one host
as a member of the `external_elasticsearch` group (nested inside the `external`
group) as follows:

```yaml
all:
  children:
    external_elasticsearch:
      hosts:
        whatever.eu-west-1.es.amazonaws.com:
          elasticsearch_username: admin
          elasticsearch_port: 9200
          elasticsearch_protocol: http # or https with port 443
    external:
      children:
        external_elasticsearch:
```

Every hosts under the `external` group is not directly managed by the acs
playbook and is required in the inventory just for the sake of architecture description.

### External Identity

Support for external Identity service will be implemented in a future playbook release (internal ref: OPSEXP-2353).

### Custom Keystore

By default the playbook deploys a default keystore to ease the installation
process, however, we recommend you [generate your own keystore][alf-keystores]
following the [instructions here][keystore-generation].

There are three steps required to use a custom keystore:

1. Place your generated keystore file in the `configuration_files/keystores` folder (these get copied to /var/opt/alfresco/content-services/keystore)
2. Override the `repository_use_custom_keystores` variable defined in your inventory as a `repository` group variable.
3. Override the `repository_acs_environment` variable and define your custom JAVA_TOOL_OPTIONS configuration
4. Add `repo_custom_keystore_password` and `repo_custom_keystore_metadata_password` in `vars/secrets.yml`

An example snippet of inventory file is shown below:

```yaml
repository:
  vars:
    repository_use_custom_keystores: true
    repository_acs_environment:
      JAVA_OPTS:
        - -Xms512m
        - -Xmx3g
        - -XX:+DisableExplicitGC
        - -Djava.awt.headless=true
        - -XX:ReservedCodeCacheSize=128m
        - $JAVA_OPTS"
      JAVA_TOOL_OPTIONS:
        - -Dencryption.keystore.type=pkcs12
        - -Dencryption.cipherAlgorithm=AES/CBC/PKCS5Padding
        - -Dencryption.keyAlgorithm=AES
        - -Dencryption.keystore.location=/var/opt/alfresco/content-services/keystore/<your-keystore-file>
        - -Dmetadata-keystore.metadata.algorithm=AES"
```

### Specifying a different component repository

In case you want to use a different server/repository for a specific artifact to further customize your deployment, you can override the default URL in two ways:

You can change the value of `component.repository` key for the selected component, provided that the path to your custom artifact follows the conventional [Maven2 Repository Layout](https://maven.apache.org/repository/layout.html). For example to change the repository of ACS artifact you would:

Edit `playbooks/group_vars/repository.yml`:

```yaml
acs_play_repository_acs_artifact_name: alfresco-content-services-distribution
acs_play_repository_acs_repository: "{{ nexus_repository.enterprise_releases }}"
```

to

```yaml
acs_play_repository_acs_artifact_name: my-own-alfresco-content-services-distribution
acs_play_repository_acs_repository: "https://your.repo.com/path/to/your/artifacts"

```

> This assumes that the full URL to your custom artifact looks like `https://your.repo.com/path/to/your/artifacts/7.2.1/alfresco-content-services-distribution-7.2.1.zip`

In case you want to install a different (not latest) ACS version, you should make similar changes to the respective `*-extra-vars.yml` file.

The other way is to override the URL completely:

In `playbooks/group_vars/repository.yml` you need to find the vars in which the default download URL for the specific artifact

```yaml
acs_play_repository_acs_archive_url: "https://your.repo.com/path/to/your/artifacts/your-alfresco-content-services-community-distribution.zip"
acs_play_repository_acs_archive_checksum: "sha1:https://your.repo.com/path/to/your/artifacts/your-alfresco-content-services-community-distribution.zip.sha1"
```

You can change url for any artifact using this approach. Just look for it inside `playbooks/group_vars/*.yml` files

## Localhost Deployment

The diagram below shows the result of a localhost deployment.

```mermaid
graph LR
user[👤] --> playbook
subgraph CN[Control Node]
  playbook(Playbooks)
  activemq[ActiveMQ]
  elasticsearch[ElasticSearch]
  nginx[Nginx]
  repository[Repository]
  postgres[Postgres]
  search_enterprise[Search Enterprise]
  sfs[Shared File Store]
  sync[Sync Service]
  transformers[AIO Transform Engine]
  trouter(Transform Router)
end
playbook --> activemq
playbook --> elasticsearch
playbook --> nginx
playbook --> repository
playbook --> postgres
playbook --> search_enterprise
playbook --> sfs
playbook --> sync
playbook --> transformers
playbook --> trouter
```

To deploy ACS 23.1 Enterprise on the local machine navigate to the folder you extracted the ZIP to and execute the playbook as the current user using the following command (the playbook will escalate privileges when required):

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_local.yml
```

Alternatively, to deploy an ACS Enterprise 7.4 system use the following command:

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_local.yml -e "acs_play_major_version=74"
```

Or to deploy ACS Community use the following command:

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_local.yml -e "acs_play_repository_acs_edition=Community"
```

By default, the ACS playbook will now also check compatibility of OS if it is  fully supported.
You can add flag '-e skip_os_test=true' if you want to deploy on not supported OS distribution.

> NOTE: The playbook takes around 30 minutes to complete.

Once the playbook is complete Ansible will display a play recap to let you know that everything is done, similar to the block below:

```bash
PLAY RECAP *******************************************************************************************************
acc_1                      : ok=24   changed=6    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0
activemq_1                 : ok=24   changed=0    unreachable=0    failed=0    skipped=17   rescued=0    ignored=0
adw_1                      : ok=24   changed=6    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0
database_1                 : ok=20   changed=0    unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
nginx_1                    : ok=21   changed=8    unreachable=0    failed=0    skipped=8    rescued=0    ignored=0
repository_1               : ok=92   changed=43   unreachable=0    failed=0    skipped=14   rescued=0    ignored=0
search_1                   : ok=34   changed=13   unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
syncservice_1              : ok=39   changed=18   unreachable=0    failed=0    skipped=13   rescued=0    ignored=0
transformers_1             : ok=81   changed=10   unreachable=0    failed=0    skipped=44   rescued=0    ignored=0
```

Once ACS has initialized access the system using the following URLs with a browser:

* Digital Workspace: `http://<control-node-public-ip>/workspace` (Enterprise Only)
* Share: `http://<control-node-public-ip>/share`
* Repository: `http://<control-node-public-ip>/alfresco`
* API Explorer: `http://<control-node-public-ip>/api-explorer`
* Control Center: `http://<control-node-public-ip>/control-center` (Enterprise Only)
* Sync Service: `http://<control-node-public-ip>/syncservice` (Enterprise Only)

## SSH Deployment

To deploy to hosts other than the control node an SSH connection is required. The control node must have network access to all the target hosts and permission to SSH into the machine.

The inventory file (`inventory_ssh.yml`) is used to specify the target IP addresses and the SSH connection details. You can specify one IP address for all the hosts to obtain a single-machine deployment, or different IP addresses for a multi-machine deployment.

The example snippet below demonstrates how to deploy the repository to a host with an IP address of `50.6.51.7` and SSH key at `/path/to/id_rsa`.

```yaml
repository:
  hosts:
    repository.acme.local:
      ansible_host: 50.6.51.7
      ansible_private_key_file: "/path/to/id_rsa"
```

If you want to deploy everything to a single machine follow the steps in the [Single Machine Deployment](#single-machine-deployment) section, alternatively, to deploy to any number of separate machines follow the steps in the [Multi Machine Deployment](#multi-machine-deployment) section.

### Single Machine Deployment

The diagram below shows the result of a single machine deployment.

```mermaid
graph LR
user[👤] --> playbook
subgraph CN[Control Node]
  playbook(Playbooks)
end
subgraph TN[Target Node]
  activemq[ActiveMQ]
  elasticsearch[ElasticSearch]
  nginx[Nginx]
  repository[Repository]
  postgres[Postgres]
  search_enterprise[Search Enterprise]
  sfs[Shared File Store]
  sync[Sync Service]
  transformers[AIO Transform Engine]
  trouter(Transform Router)
end
playbook --> TN
```

Once you have prepared the target host and configured the inventory_ssh.yaml file you are ready to run the playbook.

To check your inventory file is configured correctly and the control node is able to connect to the target host navigate to the folder you extracted the ZIP to and run the following command:

```bash
pipenv run ansible all -m ping -i inventory_ssh.yml
```

To deploy latest ACS Enterprise on the target host execute the playbook as the current user using the following command:

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_ssh.yml
```

Alternatively, to deploy an ACS 7.4 Enterprise system use the following command:

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_ssh.yml -e "acs_play_major_version=74"
```

Or to deploy latest ACS Community use the following command:

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_ssh.yml -e "acs_play_repository_acs_edition=Community"
```

> NOTE: The playbook takes around 30 minutes to complete.

Once the playbook is complete Ansible will display a play recap to let you know that everything is done, similar to the block below:

```bash
PLAY RECAP *******************************************************************************************************
acc_1                      : ok=24   changed=6    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0
activemq_1                 : ok=24   changed=0    unreachable=0    failed=0    skipped=17   rescued=0    ignored=0
adw_1                      : ok=24   changed=6    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0
database_1                 : ok=20   changed=0    unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
nginx_1                    : ok=21   changed=8    unreachable=0    failed=0    skipped=8    rescued=0    ignored=0
repository_1               : ok=92   changed=43   unreachable=0    failed=0    skipped=14   rescued=0    ignored=0
search_1                   : ok=34   changed=13   unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
syncservice_1              : ok=39   changed=18   unreachable=0    failed=0    skipped=13   rescued=0    ignored=0
transformers_1             : ok=81   changed=10   unreachable=0    failed=0    skipped=44   rescued=0    ignored=0
```

Once ACS has initialized access the system using the following URLs with a browser:

* Digital Workspace: `http://<target-host-ip>/workspace` (Enterprise Only)
* Share: `http://<target-host-ip>/share`
* Repository: `http://<target-host-ip>/alfresco`
* API Explorer: `http://<target-host-ip>/api-explorer`
* Control Center: `http://<target-host-ip>/control-center` (Enterprise Only)
* Sync Service: `http://<target-host-ip>/syncservice` (Enterprise Only)

### Multi Machine Deployment

The diagram below shows the result of a multi machine deployment.

```mermaid
graph LR
user[👤] --> playbook
subgraph CN[Control Node]
  playbook(Playbooks)
end
subgraph database_node
  postgres[Postgres]
end
subgraph repository_node
  repository[Repository]
end
subgraph activemq_node
  activemq[ActiveMQ]
end
subgraph search_node
  elasticsearch[ElasticSearch]
  search_enterprise[Search Enterprise]
end
subgraph nginx_node
  nginx[Nginx]
end
subgraph acc_node
  acc[Control Center]
end
subgraph adw_node
  adw[Digital Workspace]
end
subgraph sync_node
  sync[Sync Service]
end
subgraph transformers_node
  transformers[AIO Transform Engine]
  trouter(Transform Router)
  sfs[Shared File Store]
end
playbook --> database_node
playbook --> repository_node
playbook --> activemq_node
playbook --> search_node
playbook --> nginx_node
playbook --> acc_node
playbook --> adw_node
playbook --> sync_node
playbook --> transformers_node
```

Once you have prepared the target hosts (ensuring the [relevant ports](#tcp-port-configuration) are accessible) and configured the inventory_ssh.yaml file you are ready to run the playbook.

To check your inventory file is configured correctly and the control node is able to connect to the target hosts run the following command:

```bash
ansible all -m ping -i inventory_ssh.yml
```

**Optional** To check if the required ports for the deployment are available on the target machine and we also have connectivity between nodes (ex. repository connecting to the db on 5432) the prerun-network-checks playbook can be executed before you deploy ACS. If there are any firewalls blocking connectivity this playbook will discover them.

```bash
pipenv run ansible-playbook playbooks/prerun-network-checks.yml -i inventory_ssh.yml [-e "acs_play_repository_acs_edition=Community"]
```

To deploy latest ACS Enterprise on the target hosts execute the playbook as the current user using the following command:

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_ssh.yml
```

Or to deploy latest ACS Community use the following command:

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_ssh.yml -e "acs_play_repository_acs_edition=Community"
```

> NOTE: The playbook takes around 30 minutes to complete.

Once the playbook is complete Ansible will display a play recap to let you know that everything is done, similar to the block below:

```bash
PLAY RECAP *******************************************************************************************************
acc_1                      : ok=24   changed=6    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0
activemq_1                 : ok=24   changed=0    unreachable=0    failed=0    skipped=17   rescued=0    ignored=0
adw_1                      : ok=24   changed=6    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0
database_1                 : ok=20   changed=0    unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
nginx_1                    : ok=21   changed=8    unreachable=0    failed=0    skipped=8    rescued=0    ignored=0
repository_1               : ok=92   changed=43   unreachable=0    failed=0    skipped=14   rescued=0    ignored=0
search_1                   : ok=34   changed=13   unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
syncservice_1              : ok=39   changed=18   unreachable=0    failed=0    skipped=13   rescued=0    ignored=0
transformers_1             : ok=81   changed=10   unreachable=0    failed=0    skipped=44   rescued=0    ignored=0
```

Once ACS has initialized access the system using the following URLs with a browser:

* Digital Workspace: `http://<nginx-host-ip>/workspace` (Enterprise Only)
* Share: `http://<nginx-host-ip>/share`
* Repository: `http://<nginx-host-ip>/alfresco`
* API Explorer: `http://<nginx-host-ip>/api-explorer`
* Control Center: `http://<nginx-host-ip>/control-center` (Enterprise Only)
* Sync Service: `http://<nginx-host-ip>/syncservice` (Enterprise Only)

### Additional command switches for ansible-playbook

There are some useful argument you can use with `ansible-playbook` command in many circumstances. Some are highlighted below but take a look at [The ansible-playbook documentation](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html) for complete list of options.

* `-k` : Prompt for SSH password. Useful when no SSH keys have been deployed but needs to be th same on all hosts (prefer SSH whenever possible)
* `-K` : Prompt for sudo password. Useful when the user used to connect to the machine is not root
* `-e` : Pass an extra variable or override an existing one (read from file with `-e @file`).
* `-l` : Limit the play to a subset of hosts (either groups or individuals hosts or a mix of both)
* `-u user` : specify the username to use to connect to all targets (Prefer adding the `ansible_ssh_user` to the inventory file in the right scope, e.g. under the `all`group)

## ACS cluster

Due to load or high availability needs, you might want to deploy a cluster of
several repository nodes. This can be achieved rather simply by:

* Giving the playbook the location of the shared storage used for the ACS
  contentstore (See [Shared storage documentation](shared-contentstore.md) for
  details).
* Specifying several hosts within the repository hosts group

> :warning: as mention in the
> [Alfresco official documentation][redundancy],
> "All the servers in a cluster should have static IP addresses assigned to
> them".

For example in the inventory file:

```yaml
...
    repository:
      hosts:
        ecm1.infra.local:
        ecm2.infra.local:
        ingester.infra.local:
          repository_cluster_keepoff: true
...
```

In the `group_vars/repository.yml` file:

```yaml
...
cs_storage:
  type: nfs
  device: nas.infra.local:/exports/contentstore
  options: _netdev,noatime,nodiratim
...
```

In some circumstances, you may want to have a repo node that's dedicated to a scheduled task (such as ingesting massive amount of documents). Depending on the nature of the task and the requirements of your organisation, it may be preferable to not make this node part of the ACS cluster.
In that case, you can add the `repository_cluster_keepoff` variable to one of the `repository` group nodes'. It will provision the node with the repository and share services but make sure it not taking part in neither the share, nor the repository cluster realm.

> A typical use case is to have a dedicated Solr tracking node. The playbook will then prefer to use that dedicated node - if it finds one - for solr tracking and only use the other as backup server (no load balancing)

## Maintenance

After the initial deploy, may arise the need to execute maintenance tasks that are handled via specific playbooks.

### Search Enterprise Reindexing

You can trigger the reindexing of existing content in Search Enterprise using a dedicated playbook:

```bash
pipenv run ansible-playbook playbooks/search-enterprise-reindex.yml -i <inventory_file>.yml
```

## Cleanup and uninstall ACS

What needs to be removed from a system will depend on your inventory configuration. The steps below presume a cleanup and uninstallation of Alfresco content service after deployment of ansible artifacts by using platform-cleanup.yml playbook and platform-uninstall.yml playbook respectively.

### Cleanup

This playbook will remove the temporary artifacts which are stored on the hosts.In order to cleanup the system post deployment run the following command:

```bash
pipenv run ansible-playbook playbooks/platform-cleanup.yml -i <inventory_file>.yml
```

> Note: This playbook can break the idempotency i.e Downloaded artifacts again needs to removed by running cleanup playbook.

### Uninstallation

This playbook will uninstall the sevices which belong to the specific hosts. Below are the services, packages & folders we are removing when uninstalling

1. Stopping and removing the following services:
   * alfresco-transform-router.service
   * alfresco-shared-fs.service
   * alfresco-tengine-aio.service
   * alfresco-sync.service
   * alfresco-search.service
   * alfresco-content.service
   * nginx.service
   * activemq.service
   * postgresql-`version`.service (where `version` is 15 for ACS 23 and 14 for 7.3 & 7.4)

2. Remove the following packages:
   * ImageMagick
   * libreoffice
   * nginx
   * postgresql

3. Remove the following folders:
   * /opt/apache-activemq-`version`
   * /opt/apache-tomcat-`version`
   * /opt/libreoffice`version`
   * /opt/openjdk-`version`
   * /opt/alfresco
   * /etc/opt/alfresco
   * /var/opt/alfresco
   * /var/log/alfresco
   * /tmp/ansible_artefacts
   * /tmp/Alfresco

In order to uninstall this from the hosts run the following command:

```bash
pipenv run ansible-playbook playbooks/platform-uninstall.yml -i inventory_ssh.yml
```

## Known Issues

* The playbook downloads several large files so you will experience some pauses while they transfer and you'll also see the message "FAILED - RETRYING: Verifying if `<file>` finished downloading (nnn retries left)" appearing many times. Despite the wording this is **not** an error so please ignore and be patient!
* The playbook is not yet fully idempotent so may cause issues if you make changes and run multiple times
* The `firewalld` service can prevent the playbook from completing successfully if it's blocking the [ports required](#tcp-port-configuration) for communication between the roles
* The nginx and adw roles need to be deployed to the same host otherwise the [playbook fails](#nginx-failure)

## Troubleshooting

### Failed Downloads

If you see an error similar to the one below (in particular the mention of `HTTP Error 401: Unauthorized` or `HTTP Error 401: basic auth failed`) you've most likely forgotten to setup your Nexus credentials or mis-configured them.

```bash
fatal: [transformers_1]: FAILED! => {"msg": "An unhandled exception occurred while templating '{u'acs_zip_sha1_checksum': u\"{{ lookup('url', '{{ nexus_repository.enterprise_releases }}org/alfresco/alfresco-content-services-distribution/{{ acs_play_repository_acs_version }}/alfresco-content-services-distribution-{{ acs_play_repository_acs_version }}.zip.sha1', username=lookup('env', 'NEXUS_USERNAME'), password=lookup('env', 'NEXUS_PASSWORD')) }}\", u'adw_zip_sha1_checksum': u\"{{ lookup('url', '{{ nexus_repository.enterprise_releases }}/org/alfresco/alfresco-digital-workspace/{{ adw.version }}/alfresco-digital-workspace-{{ adw.version }}.zip.sha1', username=lookup('env', 'NEXUS_USERNAME'), password=lookup('env', 'NEXUS_PASSWORD')) }}\", u'acs_zip_url': u'{{ nexus_repository.enterprise_releases }}org/alfresco/alfresco-content-services-distribution/{{ acs_play_repository_acs_version }}/alfresco-content-services-distribution-{{ acs_play_repository_acs_version }}.zip'
...
...
Error was a <class 'ansible.errors.AnsibleError'>, original message: An unhandled exception occurred while running the lookup plugin 'url'. Error was a <class 'ansible.errors.AnsibleError'>, original message: Received HTTP error for https://artifacts.alfresco.com/nexus/service/local/repositories/enterprise-releases/content/org/alfresco/alfresco-content-services-distribution/7.0.0/alfresco-content-services-distribution-7.0.0.zip.sha1 : HTTP Error 401: Unauthorized"}
```

### Nginx Failure

If the playbook fails not being able to start Nginx, make sure both ADW and Nginx point to the same host in the inventory file. Otherwise you'll encounter the error below:

> TASK [../roles/adw : Ensure nginx service is running as configured.] *********
> fatal: [adw_1]: FAILED! => {"changed": false, "msg": "Unable to start service nginx: Job for nginx.service failed because the control process exited with error code.
> See "systemctl status nginx.service" and "journalctl -xe" for details.\n"}

### Communication Failures

If you are using a multi-machine deployment and the playbook fails with an error similar to the one shown below you may need to check the firewall configuration on the target hosts.

> TASK [../roles/repository : Notify alfresco content service] *****************
> fatal: [repository_1]: FAILED! => {"changed": false, "elapsed": 300, "msg": "Timeout when waiting for 192.168.0.126:5432"}

Either disable the firewall completely or refer to the [ports configuration](#tcp-port-configuration) section for what ports need to be accessible.

Presuming you are using `firewalld` the following example commands can be used to open a port, replacing `<port-number>` with the approriate number or replacing `<service-name>` with a well know service name e.g. "http".

```bash
firewall-cmd --permanent --add-port=<port-number>/tcp
```

or

```bash
firewall-cmd --permanent --add-service=<service-name>
```

> After the firewall config has been set up a reload of the `firewalld` service is needed

If you are using a host that is behind a proxy you might experience timeouts or `HTTP Error 401: Unauthorized` errors.

A possible quick fix is to make `http_proxy` and `https_proxy` available to either current user or to the entire system.

```bash
export http_proxy=<protocol><proxy_address>
export https_proxy=<protocol><proxy_address>
```

or add the values in the `/etc/environment`

```bash
echo http_proxy=<protocol><proxy_address> >> /etc/environment
echo https_proxy=<protocol><proxy_address> >> /etc/environment
```

If this does not solve the issue, check the proxy configuration or contact your system administrator

### Playbook Failures

If the playbook fails for some reason try re-running it with the `-v` option, if that still doesn't provide enough information try re-running with the `-vvv` option.

### Alfresco Failures

If the playbook completes successfully but the system is not functioning the best place to start is the log files, these can be found in the `/var/log/alfresco` folder on the target hosts. Please note the nginx log files are owned by root as the nginx process is running as root so it can listen on port 80.

[upload-license]: https://support.hyland.com/r/Alfresco/Alfresco-Content-Services/25.1/Alfresco-Content-Services/Administer/Licenses/Upload-new-license
[global-properties]: https://support.hyland.com/r/Alfresco/Alfresco-Content-Services/25.1/Alfresco-Content-Services/Configure/Overview/Using-alfresco-global.properties
[databases]: https://support.hyland.com/r/Alfresco/Alfresco-Content-Services/25.1/Alfresco-Content-Services/Configure/Databases
[alf-keystores]: https://support.hyland.com/r/Alfresco/Alfresco-Content-Services/25.1/Alfresco-Content-Services/Administer/Manage-Security/Authorization/Manage-Alfresco-keystores
[keystore-generation]: https://support.hyland.com/r/Alfresco/Alfresco-Content-Services/25.1/Alfresco-Content-Services/Administer/Manage-Security/Authorization/Manage-Alfresco-keystores/Keystore-generation
[redundancy]: https://support.hyland.com/r/Alfresco/Alfresco-Content-Services/25.1/Alfresco-Content-Services/Administer/High-availability-features/Clustering/Recommendations-for-split-architecture/Scenario-Clustering-for-redundancy
