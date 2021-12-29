#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. {{ config_folder }}/setenv.sh
export JAVA_OPTS="${JAVA_OPTS} -DCORE_AIO_URL=http://${ATS_TENGINE_AIO_HOST}:{{ ports_cfg.transformers.tengine }}"
export JAVA_OPTS="${JAVA_OPTS} -DCORE_AIO_QUEUE=org.alfresco.transform.engine.aio.acs"
export JAVA_OPTS="${JAVA_OPTS} -DACTIVEMQ_URL=failover:(tcp://{{ activemq_host }}:{{ ports_cfg.activemq.openwire }})?timeout=3000"
export JAVA_OPTS="${JAVA_OPTS} -DFILE_STORE_URL=http://{{ sfs_host }}:{{ ports_cfg.sfs.http }}/alfresco/api/-default-/private/sfs/versions/1/file"
{% for key, value in trouter_environment.items() %}
export {{key}}="{{value}}"
{% endfor %}
${JAVA_HOME}/bin/java ${JAVA_OPTS} -jar ${ATS_HOME}/alfresco-transform-router-*.jar > {{ logs_folder }}/ats-atr.log
