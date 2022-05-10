# Upgrades notes for the playbook

## Unreleased version

### Secrets management

Playbook has been enhanced to ease the adoption of Ansible Vault or third-party
lookup plugins to securely store secrets.

To be able to run the playbook with the new version, you need to generate a stub
`vars/secrets.yml` with:

```bash
ansible-playbook -e vault_init=plaintext playbooks/secrets-init.yml
```

Replace now in `vars/secrets.yml` the values of the secrets you don't want to change
of your existing ACS install.

Then enable file encryption (and automatically autogenerate any missing secrets) with:

```bash
ansible-playbook --ask-vault-pass -e vault_init=encrypted_file playbooks/secrets-init.yml
```

Now remove any existing secret from `group_vars/all.yml` and/or stop providing
secret values via `-e`. From now on every `ansible-playbook` invocation should
use the `--ask-vault-pass` flag otherwise secrets decryption will fail.

To discover how to avoid having to provide manually a passphrase, use
third-party plugins and/or to learn all the new capabilities for secrets
management of the playbook please read the [Deployment guide](deployment-guide.md#secrets-management).
