#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh
{% for key, value in sfs_environment.items() %}
export {{key}}="{{value}}"
{% endfor %}
${JAVA_HOME}/bin/java ${JAVA_OPTS} -jar ${ATS_HOME}/alfresco-shared-file-store-*.jar > {{ logs_folder }}/ats-shared-fs.log
