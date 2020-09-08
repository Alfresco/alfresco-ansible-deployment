#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh
export CATALINA_HOME=${TOMCAT_HOME}
export CATALINA_BASE=/etc/opt/alfresco/tomcat
export CATALINA_OPTS="-Xms2g -Xmx2g -Djava.net.preferIPv4Stack=true"
export CATALINA_TMPDIR=/var/opt/alfresco/tomcat/temp
export CATALINA_PID=/var/opt/alfresco/tomcat.pid
export LOG_BASE=/var/log/alfresco
/bin/bash -c "cd ${LOG_BASE}; ${CATALINA_HOME}/bin/catalina.sh $*"
