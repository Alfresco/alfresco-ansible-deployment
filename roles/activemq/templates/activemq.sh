#!/bin/sh
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. {{ config_folder }}/setenv.sh
export ACTIVEMQ_BASE="{{ activemq_base }}"
export ACTIVEMQ_DATA="{{ activemq_data }}"
export ACTIVEMQ_TMP="{{ activemq_tmp }}"
export ACTIVEMQ_USER="{{ username }}"
export ACTIVEMQ_PIDFILE={{ data_folder }}/activemq.pid
export ACTIVEMQ_OPTS="-Djava.util.logging.config.file=logging.properties -Djava.security.auth.login.config=${ACTIVEMQ_CONF}/login.config"
export ACTIVEMQ_OPTS="${ACTIVEMQ_OPTS} -Djava.net.preferIPv4Stack=true"
export ACTIVEMQ_OPTS="${ACTIVEMQ_OPTS} -Dactivemq.log={{ logs_folder }}"
{% for key, value in activemq_environment.items() %}
export {{ key }}="{{ value | join(' ') }}"
{% endfor %}
${ACTIVEMQ_HOME}/bin/activemq $*
