#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. {{ config_folder }}/setenv.sh
export CATALINA_HOME=${TOMCAT_HOME}
export CATALINA_BASE={{ config_folder }}/tomcat
export CATALINA_TMPDIR={{ data_folder }}/tomcat/temp
export CATALINA_PID={{ data_folder }}/tomcat.pid
export LOG_BASE={{ logs_folder }}
/bin/bash -c "cd ${LOG_BASE}; ${CATALINA_HOME}/bin/catalina.sh $*"
