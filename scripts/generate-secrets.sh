#!/bin/bash -e
SECRET_KEYS=(repo_db_password sync_db_password reposearch_shared_secret)

for SECRET_KEY in "${SECRET_KEYS[@]}"; do
    RANDOM_STRING=$(openssl rand -base64 33)
    if [ -z "${ANSIBLE_VAULT_PASSWORD_FILE}" ] || [ "$1" == 'plaintext' ]; then
        echo "${SECRET_KEY}: \"$RANDOM_STRING\""
    else
        ansible-vault encrypt_string "$RANDOM_STRING" --name "${SECRET_KEY}" | grep -v 'Encryption successful'
    fi
done
