# Pipenv developers' guide

This page describes how to use pipenv library and pipenv commands when you are developing on this repository.

## Basic pipenv knowledge

The general purpose of pipenv is similar to that of Package installer for Python (PIP) and built-in venv.
This is external python library, which handles package installing from either commandline
(with special pipenv prefix in shell, similar to pip install), requirements.txt or Pipfile.
Whether we install one package or dependencies from requirements.txt, pipenv creates Pipfile, a special file for itself,
and then installs packages we specified inside virtual environment, NOT globally.
While specifyng new package, pipenv adds that package name to Pipfile, installs it (while also generating hashcodes for .lock file)
and installs it inside virtual environment. Then we can also use this package we have installed.
The default virtual environment is created in our working directory.

> NOTE: Pipenv does not install packages globally but to virtual environment

## Basic pipenv commands and usage for developers

Pipenv comes with bunch of commands, but the most important are highlighted below:

```bash
pipenv install --dev
```

The command with flag --dev installs packages from Pipfile needed for developing purposes.
If you are not inside the directory where the Pipfile exists, it will create blank Pipfile and not install any package.
If you plan to work in another directory with the provided packages in Pipfile, you will have to copy that Pipfile to target directory.

```bash
pipenv shell
```

This command is opening the virtual environment, that pipenv created while installing all packages.
Once we are inside this environment, we can use all the packages which we specified in install command.
This is the environment where it is highly recommended to develop python.

> NOTE: We suggest for developers to run command pipenv shell and then use commands normally, within virtual environment
> for example: molecule test

Otherwise, if you are not planning to use virtual environment and need to just simply use molecule (or any other package),
you can use these commands which will execute them inside pipenv's virtual environment:

```bash
pipenv run package_name
```

Which runs said package in project's virtual environment, for example:

```bash
pipenv run molecule test
```

Which uses molecule package installed in virtual environment to execute test

> NOTE: This command runs the script with the specified package and then specified script inside virtual environment.
> You need to always be sure you are using pipenv run command inside directory where you have previously executed
> pipenv install command.

## Deploying ACS

To deploy ACS 7.1 Enterprise on the local machine navigate to the folder you extracted the ZIP to and execute the playbook as the current user using the following command (the playbook will escalate privileges when required):

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_local.yml
```

To deploy ACS Community use the following command:

```bash
pipenv run ansible-playbook playbooks/acs.yml -i inventory_local.yml -e "@community-extra-vars.yml"
```
