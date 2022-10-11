# Alfresco Ansible Deployment

[![community](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/community.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/community.yml) [![enterprise](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/enteprise.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/enteprise.yml)

This project provides an [Ansible](https://www.ansible.com) playbook capable of deploying Alfresco Content Services (ACS).

Ansible is an open-source software provisioning, configuration management and application-deployment tool enabling infrastructure as code.

A user runs a playbook that deploys to any number of hosts as shown in the diagram below.

![Ansible Overview](./docs/resources/ansible-overview.png)

## Prerequisites

* If you want to install the Enterprise version, Nexus credentials for [https://artifacts.alfresco.com](https://artifacts.alfresco.com)

## Documentation

Please refer to the [Documentation](./docs/README.md) for an overview of the project and the playbook or go directly to the [deployment guide](./docs/deployment-guide.md) to learn how to run the playbook.

Users upgrading from previous versions of the playbook may want to take a look to [Upgrade Notes](docs/playbook-upgrade.md).

## Development

Developer's guide is available [here](docs/developer-guide.md).

## License

The code in this repository is released under the Apache License, see the [LICENSE](./LICENSE) file for details.

## Contribution

Please use [this guide](CONTRIBUTING.md) to make a contribution to the project and information to report any issues.

### Adding support for a new distribution

We expect distribution support to be added using mostly roles `vars` files. If
distro specific tasks are needed those should be skipped for other distros
and possibly added in separate task files.

The OS support table in `docs/README.md` must be updates and so does the
`supported_os` variable in the `group_vars/all.yml` file.

## Release

To start the release process, just create a tag and push it.

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
