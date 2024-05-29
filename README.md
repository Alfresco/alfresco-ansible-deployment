# Alfresco Ansible Deployment

[![community](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/community.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/community.yml)
[![enterprise](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/enteprise.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/enteprise.yml)
[![enterprise-extended](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/enterprise-extended.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/enterprise-extended.yml)
[![release](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/release.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/release.yml)
[![pre-commit](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/precommit.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/precommit.yml)
[![Publish docs](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/docs.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/docs.yml)
[![Bump artifacts versions](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/updatecli.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/updatecli.yml)

This project provides [Ansible](https://www.ansible.com) playbooks capable of
deploying Alfresco Content Services (ACS) with different configuration flavours.

The user documentation is available on [GitHub Pages](https://alfresco.github.io/alfresco-ansible-deployment/).

## Developers guide

This page is a developers guide for to popular commands used in the process of
setting up environment for development, testing and release.

* [Alfresco Ansible Deployment](#alfresco-ansible-deployment)
  * [Developers guide](#developers-guide)
  * [Introduction to pipenv](#introduction-to-pipenv)
  * [Basic pipenv usage](#basic-pipenv-usage)
  * [Development](#development)
    * [Roles tests](#roles-tests)
    * [Integration tests](#integration-tests)
      * [Docker based tests](#docker-based-tests)
  * [Adding support for a new distribution](#adding-support-for-a-new-distribution)
  * [Release](#release)
    * [Tag and release](#tag-and-release)

## Introduction to pipenv

The general purpose of pipenv is similar to that of Package installer for Python
(PIP) and built-in venv. This is external python library, which handles package
installing from either command line (with special pipenv prefix in shell,
similar to pip install), requirements.txt or Pipfile. Whether we install one
package or dependencies from requirements.txt, pipenv creates Pipfile, a special
file for itself, and then installs packages we specified inside virtual
environment, NOT globally. While specifying new package, pipenv adds that
package name to Pipfile, installs it (while also generating hashcodes for .lock
file) and installs it inside virtual environment. Then we can also use this
package we have installed. The default virtual environment is created in our
working directory. You may want to visit: <https://pipenv.pypa.io/en/latest/>

> NOTE: Pipenv does not install packages globally but into a virtual environment

## Basic pipenv usage

Pipenv comes with bunch of commands, but the most important are highlighted
below: The command with flag --dev installs packages from Pipfile needed for
developing purposes.

```bash
pipenv install --dev --python $(cat .python-version)
```

This command below is opening the virtual environment, that pipenv created while
installing all packages. Once we are inside this environment, we can use all the
packages which we specified in install command. This is the environment where it
is highly recommended to develop python.

> NOTE: Right now it is not supported by pipenv to have two virtual environments
> in the same directory, so if you try work with two different environments
> within same directory, you will overwrite the previously created virtual
> environment

```bash
pipenv shell
```

Otherwise, if you are not planning to use virtual environment and need to just
simply use molecule (or any other package), you can use these commands which
will execute them inside pipenv's virtual environment:

```bash
pipenv run command
```

Which runs said package in project's virtual environment, for example:

```bash
pipenv run molecule test
```

Which uses molecule package installed in virtual environment to execute test

> NOTE: This command runs the script with the specified package and then
> specified script inside virtual environment. You need to always be sure you
> are using pipenv run command inside directory where you have previously
> executed pipenv install command.

## Development

The roles developed for this playbook are tested with [Molecule](https://molecule.readthedocs.io/en/latest/).

### Roles tests

> NOTE: REMEMBER THESE COMMANDS NEED TO BE USED INSIDE VIRTUAL ENVIRONMENT, IF
> NOT YOU NEED TO ADD PREFIX PIPENV RUN

You can run Molecule tests on your machine if you have a Docker Engine installed
locally.

Enter the role folder and run `molecule <action>` (see [official
docs]\(<https://molecule.readthedocs.io/en/latest/getting-started>.html#run-test-sequence-commands)).

 To provision the `activemq` role run:

```sh
cd roles/activemq
molecule converge
```

 To execute tests after converge run successfully:

```sh
molecule verify
```

 To enter the container and inspect manually the state:

```sh
molecule login
```

 To destroy the container and release resources at the end:

```sh
molecule destroy
```

 If you want to test a different operating system, set the `MOLECULE_ROLE_IMAGE`
 to a different docker base image before converging:

```sh
MOLECULE_ROLE_IMAGE=ubuntu:20.04 molecule converge
```

### Integration tests

On the root folder there are two different molecule scenarios to run the entire
playbook on EC2 instances with different operating systems (single node or
multimachine/clustered).

Some environment variables are required to execute integration tests locally,
please take a look at the [.envrc](/.envrc) file as a reference.

To have those environment variables automatically loaded when entering the
project folder on your dev machine, you may want to install
[direnv](https://direnv.net/), otherwise you can also configure them as you prefer.

When using direnv, you must add your secrets in the `.env.credentials` in the
root folder, following the standard export convention of bash. Direnv will
automatically suggest you to do that.

Scenario-specific variables are defined in the `vars-scenario.yml` files inside
the `molecule/default` folder.

To run an integration test you need execute molecule with `-e
molecule/default/vars-scenario.yml` parameter:

```bash
molecule -e molecule/default/vars-rhel8.yml test
```

#### Docker based tests

There is also a `local` molecule scenario that use the same approach of roles
molecule tests, using the docker driver.

You can run it with:

```sh
molecule -s local test
```

## Adding support for a new distribution

We expect distribution support to be added using mostly roles `vars` files. If
distro specific tasks are needed those should be skipped for other distros
and possibly added in separate task files.

New distributions must be added to the `supported_os` variable in the `group_vars/all.yml` file.

If a new OS enters the official supported matrix but is not supported by the
playbook. It must be mentioned in the [Versioning chapter of the
doc](./README.md#versioning)

## Release

Follow this quick checklist:

* review currently open dependabot/renovate and merge them
* copy the versions inside the group_vars/all.yml to a new XX.N-extra-vars.yml (in case of a new ACS major version)
* run [updatecli workflow](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/updatecli.yml)
* run [enterprise-extended](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/enterprise-extended.yml) and make sure it is green
* ensure that the [versions table in the main readme](docs/overview.md#versioning) has been updated
* ensure that docker images and AMI id for the root molecule tests are
  reflecting any eventual minor OS release (e.g. [default
  suite](../molecule/default/))

### Tag and release

To start the actual release process, just create a tag and push it.

If you have GPG setup, use `git tag -s` otherwise `git tag -a`.

Tag name must have `v` prefix.

Example with GPG sign enabled:

```bash
git tag -s v2.x.x -m v2.x.x
```

Then push the tag with:

```bash
git push origin v2.x.x
```

Check that the triggered [Release workflow](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/release.yml) go green.
