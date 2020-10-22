#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. {{ config_folder }}/setenv.sh
export CATALINA_HOME=${TOMCAT_HOME}
export CATALINA_BASE={{ config_folder }}/tomcat
export CATALINA_OPTS="-Xms2g -Xmx2g -Djava.net.preferIPv4Stack=true"
export CATALINA_TMPDIR={{ data_folder }}/tomcat/temp
export CATALINA_PID={{ data_folder }}/tomcat.pid
export LOG_BASE={{ logs_folder }}
/bin/bash -c "cd ${LOG_BASE}; ${CATALINA_HOME}/bin/catalina.sh $*"
if [ ! -z "$ATS_SHARED_FS_HOST" ]
then
    export CATALINA_OPTS="${CATALINA_OPTS} -Dats-shared-fs.host=${ATS_SHARED_FS_HOST}"
else
    export CATALINA_OPTS="${CATALINA_OPTS} -Dats-shared-fs.host={{ sfs_host }}"
fi

if [ ! -z "$ATS_TENGINE_AIO_HOST" ]
then
    export CATALINA_OPTS="${CATALINA_OPTS} -Dats-tengine-aio.host=${ATS_TENGINE_AIO_HOST}"
else
    export CATALINA_OPTS="${CATALINA_OPTS} -Dats-tengine-aio.host={{ ats_tengine_aio_host }}"
fi
