#!/bin/bash -x

if [ -n "$MOLECULE_IT_SCENARIO" ]; then
    EXTRA_CONFIG=""
    MOLECULE_IT_PATH="molecule/$MOLECULE_IT_SCENARIO"
    if [ -n "$MOLECULE_IT_CONFIG" ]; then
        EXTRA_CONFIG="-e $MOLECULE_IT_PATH/$MOLECULE_IT_CONFIG"
    fi
    if [ "$1" == 'destroy' ]; then
        # shellcheck disable=SC2086
        molecule $EXTRA_CONFIG destroy -s "$MOLECULE_IT_SCENARIO"
    elif [ "$1" == 'verify' ]; then
        # shellcheck disable=SC2086
        molecule $EXTRA_CONFIG converge -s "$MOLECULE_IT_SCENARIO" || exit 1
        # shellcheck disable=SC2086
        molecule $EXTRA_CONFIG side-effect -s "$MOLECULE_IT_SCENARIO"
        # shellcheck disable=SC2086
        molecule $EXTRA_CONFIG verify -s "$MOLECULE_IT_SCENARIO"
    else
        echo "$1: invalid command"
        exit 1
    fi
else
    echo "no molecule it scenario is set, doing nothing"
fi
