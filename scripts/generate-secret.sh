#!/bin/bash -e

usage() {
    echo "Usage: $0 -s SECRET_KEY [ -m plaintext ]" 1>&2
}
exit_abnormal() {
    usage
    exit 1
}

while getopts ":m:s:" options; do
    case $options in
    m) MODE=$OPTARG ;;
    s) SECRET_KEY=$OPTARG ;;
    *) exit_abnormal ;;
    esac
done

if [ -z "${SECRET_KEY}" ]; then
    echo SECRET_KEY must be provided
    exit_abnormal
fi

RANDOM_STRING=$(openssl rand -base64 33)
if [ -z "${ANSIBLE_VAULT_PASSWORD_FILE}" ] || [ "$MODE" == 'plaintext' ]; then
    echo "${SECRET_KEY}: \"$RANDOM_STRING\""
else
    ansible-vault encrypt_string "$RANDOM_STRING" --name "${SECRET_KEY}" | grep -v 'Encryption successful'
fi
