---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

#### Bug description

<!--
A clear and concise description of the problem you are facing and what you expected to happen instead.
-->

#### Target OS

<!--
The operating system against playbook is running
-->

#### Host OS

<!--
The operating system against playbook is running
-->

#### Playbook version

<!-- semver release or `git rev-parse HEAD` sha -->

#### Ansible error

<!--
Copy and paste the failed Ansible task while running this playbook (inside below code fences)
-->

```shell

```

#### Ansible context

<!--
Paste the output of the following commands (prefix by `pipenv run` or run within `pipenv shell`)
-->

##### ansible --version

```shell

```

##### ansible-config dump --only-changed

```shell

```

##### ansible-inventory -i your_inventory_file --graph

```shell

```

##### pip list

```shell

```
