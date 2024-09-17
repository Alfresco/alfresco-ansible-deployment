#!/bin/bash
set -e
set -o pipefail

usage() {
    echo "Usage: $0 -s SECRET_KEY -m (plaintext|plugin|encrypt_string)" 1>&2
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

export ANSIBLE_FORCE_COLOR=False
export ANSIBLE_NOCOLOR=True
export ANSIBLE_INVENTORY_UNPARSED_WARNING=False

while true; do
    RANDOM_STRING=$(
        ansible -m ansible.builtin.command \
        -a "echo {{ lookup('password','/dev/null',chars=['ascii_letters','digits','+./#@^()[_'],length=33) }}" \
        localhost -o \
        | awk '{print $NF}'
    )
    # Ensure that the generated password meet simple complexity requirements
    if [[ $RANDOM_STRING =~ [A-Z] && $RANDOM_STRING =~ [a-z] && $RANDOM_STRING =~ [0-9] && $RANDOM_STRING =~ [^A-Za-z0-9] ]]; then
        break
    fi
done

if [ "$MODE" == 'plaintext' ]; then
    echo "${SECRET_KEY}: \"$RANDOM_STRING\""
elif [ "$MODE" == 'plugin' ]; then
    echo "${SECRET_KEY}: \"{{ lookup('') }}\""
elif [ "$MODE" == 'encrypt_string' ]; then
    ansible-vault encrypt_string "$RANDOM_STRING" --name "${SECRET_KEY}" | grep -v 'Encryption successful'
else
    echo MODE "$MODE" is not supported
    exit_abnormal
fi
