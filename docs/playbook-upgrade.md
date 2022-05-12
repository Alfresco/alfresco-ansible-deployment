# Upgrades notes for the playbook

## Unreleased version

### Secrets management

Playbook has been enhanced to ease the adoption of Ansible Vault or third-party
lookup plugins to securely store secrets.

To be able to run the playbook with the new version, all the secrets needs to be
moved inside the `vars/secrets.yml`:

```yml
repo_db_password: ""
sync_db_password: ""
reposearch_shared_secret: ""
activemq_password: ""
```

If you are managing a test environment, you can proceed as usual just by setting
the `test_environment` variable to `true` the next time you run the playbook.

If you are managing a production environment and you want to reuse them same
credentials, paste them in the `vars/secrets.yml` and remove them from
`group_vars/all.yml` or anywhere you are providing them.

If you want to regenerate all the passwords for best security, just go ahead.

To enable secrets file encryption, with a password supplied manually before each run:

```bash
ansible-playbook --ask-vault-pass -e vault_init=encrypted_file playbooks/secrets-init.yml
```

From now on every standard `ansible-playbook` invocation should use the
`--ask-vault-pass` flag otherwise secrets decryption will fail.

To discover how to avoid having to provide manually a passphrase, use
third-party plugins and/or to learn all the new capabilities for secrets
management of the playbook please read the [Deployment guide](deployment-guide.md#secrets-management).
