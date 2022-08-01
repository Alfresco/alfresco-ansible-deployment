#!/bin/bash

PIP_MODULES=$(pip3 freeze)

declare -a module_names=( "ansible-core" "Jinja2" )
declare -a module_versions=( "2.12.7" "3.1.2" )


for index in "${!module_names[@]}"; do

  REQ_MODULE_NAME="${module_names[$index]}"
  REQ_MODULE_VERSION_FULL="${module_versions[$index]}"
  IFS='.' read -ra REQ_MODULE_VERSION <<< "$REQ_MODULE_VERSION_FULL"

  PIP_MODULE=$(echo "$PIP_MODULES" | grep "${REQ_MODULE_NAME}"==)
  if [ -z "$PIP_MODULE" ]; then 
    echo "${REQ_MODULE_NAME} not found";
    exit 1 
  fi

  IFS='==' read -ra PIP_MODULE <<< "$PIP_MODULE"
  PIP_MODULE_NAME="${PIP_MODULE[0]}"
  PIP_MODULE_VERSION_FULL="${PIP_MODULE[2]}"
  IFS='.' read -ra PIP_MODULE_VERSION <<< "$PIP_MODULE_VERSION_FULL"
  if [[ $((PIP_MODULE_VERSION[0])) -lt $((REQ_MODULE_VERSION[0])) ]] ||
     [[ $((PIP_MODULE_VERSION[1])) -lt $((REQ_MODULE_VERSION[1])) ]] ||
     [[ ${REQ_MODULE_VERSION[2]} && $((PIP_MODULE_VERSION[2])) -lt $((REQ_MODULE_VERSION[2])) ]]; then
    a="Unsupported $PIP_MODULE_NAME version: $PIP_MODULE_VERSION_FULL."
    b="Upgrade to at least $REQ_MODULE_VERSION_FULL to avoid errors during deployment"
    echo "$a" "$b"
    exit 2
  fi
done
