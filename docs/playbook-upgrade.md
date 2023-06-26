# Upgrades notes for the playbook

## Unreleased version

### Passing Alfresco global properties

In previous version we provided an empty `alfresco-global.properties` file to
conveniently pass static configuration for ACS repository. We're deprecating
this.
Instead we now accept a list of file(s) that can be passed to the `repository`
role as a role argument. Within the role the default value of the argument
(`raw_properties`) is empty, but the playbook sets a values for it using
`repository` group vars. This ensure backward compatibility for now, but be
aware that we will remove this from next major version.

The newer approach is just to use the `global_properties` in the `repository`
group var as much as possible, and if you really need to include a snippet of
properties from a file, reference this file in the `properties_snippets` in
the same `repository` group vars (which will be passed automatically by the
playbook to the `raw_properties` role argument).

## v2.1.0

### Secrets management

Playbook has been enhanced to ease the adoption of Ansible Vault or third-party
lookup plugins to securely store secrets.

To be able to run the playbook with the new version, all the secrets needs to be
moved inside the `vars/secrets.yml` with a set of known keys:

```yml
repo_db_password: ""
sync_db_password: ""
reposearch_shared_secret: ""
activemq_password: ""
```

If you are managing a test environment and don't want to bother manually
configuring passwords, you can proceed as usual just by setting the
`autogen_unsecure_secrets` variable to `true` in `group_vars/all.yml`. In this
way secrets will be auto-generated but will be saved on your file-system in
plain text as in the previous versions of the playbook.

If you are managing a production environment and you want to reuse them same
credentials, fill the `vars/secrets.yml` accordingly and remove them from
`group_vars/all.yml` or anywhere you are providing them.

To enable secrets file encryption you can run the `secrets-init.yml` playbook,
that is also generating any missing secret automatically. The encryption is
using a password supplied manually before each run.

```bash
ansible-playbook --ask-vault-pass -e vault_init=encrypted_file playbooks/secrets-init.yml
```

From now on every standard `ansible-playbook` invocation should use the
`--ask-vault-pass` flag otherwise secrets decryption will fail.

To discover how to avoid having to provide manually a passphrase, use
third-party plugins and/or to learn all the new capabilities for secrets
management of the playbook please read the [Deployment guide](deployment-guide.md#secrets-management).
