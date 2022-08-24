# Developers' guide

This page is a developer's guide to popular commands used in the process of setting up environment and testing.

## Basic pipenv knowledge

The general purpose of pipenv is similar to that of Package installer for Python (PIP) and built-in venv.
This is external python library, which handles package installing from either commandline (with special pipenv prefix in shell, similar to pip install), requirements.txt or Pipfile.
Whether we install one package or dependencies from requirements.txt, pipenv creates Pipfile, a special file for itself,
and then installs packages we specified inside virtual environment, NOT globally.
While specifyng new package, pipenv adds that package name to Pipfile, installs it (while also generating hashcodes for .lock file)
and installs it inside virtual environment. Then we can also use this package we have installed.
The default virtual environment is created in our working directory. You may want to visit: <https://pipenv.pypa.io/en/latest/>

> NOTE: Pipenv does not install packages globally but to virtual environment

## Basic pipenv commands and usage for developers

Pipenv comes with bunch of commands, but the most important are highlighted below:
The command with flag --dev installs packages from Pipfile needed for developing purposes.

```bash
pipenv install --dev
```

This command below is opening the virtual environment, that pipenv created while installing all packages.
Once we are inside this environment, we can use all the packages which we specified in install command.
This is the environment where it is highly recommended to develop python.

```bash
pipenv shell
```

> NOTE: We suggest for developers to run command pipenv shell and then use commands normally, within virtual environment
> for example: molecule test

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

On the root folder there is a molecule scenario to run the entire playbook on EC2 instances with different operating systems.

Some environment variables are required to execute integration tests locally, please take a look at the [.envrc](.envrc) file.

To have environment variables automatically loaded when entering the project folder on your machine, you may want to install [direnv](https://direnv.net/).

Scenario-specific variables are defined in the `vars-scenario.yml` files inside the `molecule/default` folder.

To run an integration test you need execute molecule with `-e molecule/default/vars-scenario.yml` parameter:

```bash
molecule -e molecule/default/vars-rhel8.yml test
```
