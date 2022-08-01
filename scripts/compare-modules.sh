#!/bin/bash

PIP_MODULES=$(pip3 freeze)

while read -r LINE; do

  IFS='==' read -ra REQ_MODULE <<< "$LINE"
  REQ_MODULE_NAME="${REQ_MODULE[0]}"
  IFS='.' read -ra REQ_MODULE_VERSION <<< "${REQ_MODULE[2]}"
  REQ_MODULE_VERSION_FULL="${REQ_MODULE_VERSION[0]}.${REQ_MODULE_VERSION[1]}.${REQ_MODULE_VERSION[2]}"

  PIP_MODULE=$(echo $PIP_MODULES | tr ' ' '\n' | grep ${REQ_MODULE_NAME}==)
  if [ -z $PIP_MODULE ]; then 
    echo "${REQ_MODULE_NAME} not found";
    exit 1 
  fi

  IFS='==' read -ra PIP_MODULE <<< "$PIP_MODULE"
  PIP_MODULE_NAME="${PIP_MODULE[0]}"
  IFS='.' read -ra PIP_MODULE_VERSION <<< "${PIP_MODULE[2]}"
  if [[ $((${PIP_MODULE_VERSION[0]})) -lt $((${REQ_MODULE_VERSION[0]})) ]] ||
     [[ $((${PIP_MODULE_VERSION[1]})) -lt $((${REQ_MODULE_VERSION[1]})) ]] ||
     [[ ${REQ_MODULE_VERSION[2]} && $((${PIP_MODULE_VERSION[2]})) -lt $((${REQ_MODULE_VERSION[2]})) ]]; then
    echo "Unsupported $PIP_MODULE_NAME version. Upgrade to at least $REQ_MODULE_VERSION_FULL to avoid errors during deployment"
    exit 2
  fi
done < ../requirements.txt
