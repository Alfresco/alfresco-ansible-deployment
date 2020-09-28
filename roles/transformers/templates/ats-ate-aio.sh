#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh
export JAVA_OPTS="${JAVA_OPTS} -DPDFRENDERER_EXE=${ACS_HOME}/alfresco-pdf-renderer/alfresco-pdf-renderer"
export JAVA_OPTS="${JAVA_OPTS} -DLIBREOFFICE_HOME=${LIBREOFFICE_HOME}"
export JAVA_OPTS="${JAVA_OPTS} -DIMAGEMAGICK_ROOT=${IMAGEMAGICK_HOME} -DIMAGEMAGICK_DYN=${IMAGEMAGICK_DYN} -DIMAGEMAGICK_EXE=${IMAGEMAGICK_EXE} -DIMAGEMAGICK_CONFIG=${IMAGEMAGICK_CONFIG} -DIMAGEMAGICK_CODERS=${IMAGEMAGICK_CODERS}"
export JAVA_OPTS="${JAVA_OPTS} -DACTIVEMQ_URL=failover:(tcp://${ACTIVEMQ_HOST}:61616)?timeout=3000"
${JAVA_HOME}/bin/java ${JAVA_OPTS} -jar ${ATS_HOME}/alfresco-transform-core-aio-boot-*.jar > {{ logs_folder }}/ats-ate-aio.log