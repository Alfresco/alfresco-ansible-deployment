#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh
${JAVA_HOME}/bin/java -jar ${ATS_HOME}/alfresco-shared-file-store-*.jar > /var/log/alfresco/ats-shared-fs.log