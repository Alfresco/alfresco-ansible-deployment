#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh
export JAVA_OPTS="${JAVA_OPTS} -DPDFRENDERER_EXE={{ ats_home }}/alfresco-pdf-renderer"
export JAVA_OPTS="${JAVA_OPTS} -DLIBREOFFICE_HOME=${LIBREOFFICE_HOME}"
export JAVA_OPTS="${JAVA_OPTS} -DIMAGEMAGICK_ROOT=${IMAGEMAGICK_HOME} -DIMAGEMAGICK_DYN=${IMAGEMAGICK_DYN} -DIMAGEMAGICK_EXE=${IMAGEMAGICK_EXE} -DIMAGEMAGICK_CONFIG=${IMAGEMAGICK_CONFIG} -DIMAGEMAGICK_CODERS=${IMAGEMAGICK_CODERS}"
{% if acs.edition == 'Enterprise' %}
export JAVA_OPTS="${JAVA_OPTS} -DACTIVEMQ_URL=failover:(tcp://{{ activemq_host }}:61616)?timeout=3000"
export JAVA_OPTS="${JAVA_OPTS} -DFILE_STORE_URL=http://${ATS_SHARED_FS_HOST}:8099/alfresco/api/-default-/private/sfs/versions/1/file"
{% endif %}

{% for key, value in tengine_environment.items() %}
export {{key}}="{{value}}"
{% endfor %}
${JAVA_HOME}/bin/java ${JAVA_OPTS} -jar ${ATS_HOME}/alfresco-transform-core-aio-boot-*.jar > {{ logs_folder }}/ats-ate-aio.log