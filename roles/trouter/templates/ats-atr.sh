#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh
export JAVA_OPTS="${JAVA_OPTS} -DCORE_AIO_URL=http://${ATS_TENGINE_AIO_HOST}:8090"
export JAVA_OPTS="${JAVA_OPTS} -DCORE_AIO_QUEUE=org.alfresco.transform.engine.aio.acs"
export JAVA_OPTS="${JAVA_OPTS} -DACTIVEMQ_URL=failover:(tcp://{{ activemq_host }}:61616)?timeout=3000"
export JAVA_OPTS="${JAVA_OPTS} -DFILE_STORE_URL=http://{{ sfs_host }}:8099/alfresco/api/-default-/private/sfs/versions/1/file"
{% for key, value in trouter_environment.items() %}
export {{key}}="{{value}}"
{% endfor %}
${JAVA_HOME}/bin/java ${JAVA_OPTS} -jar ${ATS_HOME}/alfresco-transform-router-*.jar > /var/log/alfresco/ats-atr.log