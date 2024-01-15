# Developers guide

This page is a developers guide for to popular commands used in the process of setting up environment for development and testing.

## Basic pipenv knowledge

The general purpose of pipenv is similar to that of Package installer for Python (PIP) and built-in venv.
This is external python library, which handles package installing from either command line (with special pipenv prefix in shell, similar to pip install), requirements.txt or Pipfile.
Whether we install one package or dependencies from requirements.txt, pipenv creates Pipfile, a special file for itself,
and then installs packages we specified inside virtual environment, NOT globally.
While specifying new package, pipenv adds that package name to Pipfile, installs it (while also generating hashcodes for .lock file)
and installs it inside virtual environment. Then we can also use this package we have installed.
The default virtual environment is created in our working directory. You may want to visit: <https://pipenv.pypa.io/en/latest/>

> NOTE: Pipenv does not install packages globally but to virtual environment

## Basic pipenv commands and usage for developers

Pipenv comes with bunch of commands, but the most important are highlighted below:
The command with flag --dev installs packages from Pipfile needed for developing purposes.

```bash
pipenv install --dev --python $(cat .python-version)
```

This command below is opening the virtual environment, that pipenv created while installing all packages.
Once we are inside this environment, we can use all the packages which we specified in install command.
This is the environment where it is highly recommended to develop python.

> NOTE: Right now it is not supported by pipenv to have two virtual environments in the same directory, so if you
> try work with two different environments within same directory, you will overwrite the previously created virtual environment

```bash
pipenv shell
```

Otherwise, if you are not planning to use virtual environment and need to just simply use molecule (or any other package),
you can use these commands which will execute them inside pipenv's virtual environment:

```bash
pipenv run command
```

Which runs said package in project's virtual environment, for example:

```bash
pipenv run molecule test
```

Which uses molecule package installed in virtual environment to execute test

> NOTE: This command runs the script with the specified package and then specified script inside virtual environment.
> You need to always be sure you are using pipenv run command inside directory where you have previously executed
> pipenv install command.

## Development

The roles developed for this playbook are tested with [Molecule](https://molecule.readthedocs.io/en/latest/).

### Roles tests

> NOTE: REMEMBER THESE COMMANDS NEED TO BE USED INSIDE VIRTUAL ENVIRONMENT, IF NOT YOU NEED TO ADD PREFIX PIPENV RUN

You can run Molecule tests on your machine if you have a Docker Engine installed locally.

Enter the role folder and run `molecule <action>` (see [official docs]\(<https://molecule.readthedocs.io/en/latest/getting-started>.html#run-test-sequence-commands)).

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

 If you want to test a different operating system, set the `MOLECULE_ROLE_IMAGE` to a different docker base image before converging:

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

#### Docker integration test

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

* copy the versions inside the group_vars/all.yml to a new X.X.N-extra-vars.yml
* run updatecli against the latest and supported versions (one for each extra-vars file)
  * e.g. `updatecli apply --config scripts/updatecli/updatecli_config.tpl --values scripts/updatecli/updatecli_base.yml --values scripts/updatecli/updatecli_acs23.yml`
* ensure that the [tables in the main readme](README.md) has been updated
* ensure that AMI id for the root molecule tests are not outdated (e.g. [default suite](../molecule/default/vars-rhel8.yml))

### Bumping ACS version via updatecli

This repo provide experimental support for updatecli to keep ACS components
versions in sync with the latest ACS releases. Configurations files are in the
`scripts/updatecli` folder.

The `updatecli_config.tpl` file provides the main pipeline definition and there
are multiple values files depending on which acs major version we want to check
for any new minor release.

Run updatecli with:

```bash
updatecli apply --config scripts/updatecli/updatecli_config.tpl --values scripts/updatecli/updatecli_base.yml --values scripts/updatecli/updatecli_acsXX.yml
```

Once the command completes successfully, you will find the target file
automatically modified with the latest available versions:

* `groups_vars/all.yml`

Commit and push them on a new `next/acs-XX` branch, if you are starting to the the new pre-release versions.
If you are at release time, just raise a PR to merge in `master`.

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
