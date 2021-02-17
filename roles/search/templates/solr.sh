#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi
. {{ config_folder }}/setenv.sh
export SOLR_INCLUDE={{ config_dir }}/solr.in.sh
{{ binaries_dir }}/solr/bin/solr $*
chmod -R u+rwx,g+rw,o-rwx {{ logs_folder }}/