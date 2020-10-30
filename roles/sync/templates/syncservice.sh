#!/bin/bash
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh
USER="{{ username }}"
JAR_LOCATION=${SYNC_HOME}/service-sync
SYNC_JAR_VERSION=${SYNC_VERSION}
SYNC_JAR_CONFIG_YML_LOCATION=/etc/opt/alfresco/sync-service/config.yml
DB_CONNECTORS_FOLDER=${JAR_LOCATION}/connectors
SYNC_LOG_LOCATION=/var/log/alfresco
PID_FILE=/var/opt/alfresco/syncservice.pid
START_CMD="cd $JAR_LOCATION;$JAVA_HOME/bin/java $JMX_CONF $JAVA_OPTS -cp $DB_CONNECTORS_FOLDER/*:$SYNC_JAR_FILE org.alfresco.service.sync.dropwizard.SyncService server $SYNC_JAR_CONFIG_YML_LOCATION  $SUPPRESS_OUTPUT_CMD &"
STOP_CMD="cd $JAR_LOCATION;$JAVA_HOME/bin/java $JMX_SECURITY_CONF $JAVA_OPTS -cp $SYNC_JAR_FILE org.alfresco.service.sync.SyncServiceShutdown --stop $SUPPRESS_OUTPUT_CMD"

stop_script() {
#       if [ "${CUR_USER}" != "root" ]; then
#               log_failure_msg "You do not have permission to stop $NAME."
#               exit 1
#       fi

        eval PID="$PID_GREP_CMD"