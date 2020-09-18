#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh
export SOLR_INCLUDE={{ config_dir }}/solr.in.sh
{{ dist_dir }}/solr/bin/solr $*