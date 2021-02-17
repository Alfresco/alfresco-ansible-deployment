#!/bin/bash
if [ $(id -u) -eq 0 ]; then
    echo "This script must not be executed by root"
    exit
fi

. /etc/opt/alfresco/setenv.sh

{% for key, value in sync_environment.items() %}
{{key}}="{{value}}"
{% endfor %}

### Fill in these bits:
USER="alfresco"
### Path to service-sync jar
JAR_LOCATION=${SYNC_HOME}/service-sync
SYNC_JAR_VERSION=${SYNC_VERSION}
SYNC_JAR_FILE=service-sync-$SYNC_JAR_VERSION.jar
SYNC_JAR_CONFIG_YML_LOCATION={{ config_folder }}/sync-service/config.yml
DB_CONNECTORS_FOLDER=${JAR_LOCATION}/connectors
SYNC_LOG_LOCATION={{ logs_folder }}
NAME="alfresco-syncservice"

chmod -R u+rwx,g+rw,o-rwx $SYNC_LOG_LOCATION/

### Start of JMX config ###
### true | false
ENABLE_JMX_REMOTE=true
JMX_REMOTE_PORT=50800
### Remote JMX administration requires changing the following to the IP address of the Sync Service machine:
#Specify a value only if intended to connect from a different network than the one Sync service is in.
#Specify localhost or 127.0.0.1 if intended to be accessed only from localhost.
JMX_RMI_HOSTNAME=
JMX_REMOTE_RMI_PORT=50801

### true | false
ENABLE_JMX_REMOTE_AUTHENTICATION=false
### If you enable JMX_REMOTE_AUTHENTICATION, then, set the next two properties (ie.JMX_PASSWORD_FILE, JMX_ACCESS_FILE)
JMX_PASSWORD_FILE=/path/to/jmx.password
JMX_ACCESS_FILE=/path/to/jmx.access

### Caution - if you set 'ENABLE_JMX_REMOTE_AUTHENTICATION' and 'ENABLE_JMX_REMOTE_SSL' to false, any remote user who knows
### (or guesses) your port number and host name will be able to monitor and control your applications and platform.
### true | false
ENABLE_JMX_REMOTE_SSL=false
### If you enable JMX_REMOTE_SSL, then, set the next six properties
### The password for both out-of-the-box keyStores can be looked-up in the "server.applicationConnectors.keyStorePassword" section of the config.yml file.
### KeyStore details
SYNC_KEYSTORE=/path/to/sync.p12
SYNC_KEYSTORE_PASSWORD=store-passowrd
SYNC_KEYSTORE_TYPE=JCEKS
### TrustStore details
SYNC_TRUSTSTORE=/path/to/sync.truststore
SYNC_TRUSTSTORE_PASSWORD=store-passowrd
SYNC_TRUSTSTORE_TYPE=JCEKS
### End of JMX config ###

#Whether the output of Sync start/stop command should be suppressed or not.
#If true, then the commands' output will be printed in the console.
SYNC_VERBOSE_OUTPUT=false

### No changes required below this point
PID_FILE={{ data_folder }}/syncservice.pid
JMX_CONF="-Dcom.sun.management.jmxremote=$ENABLE_JMX_REMOTE"
JMX_SECURITY_CONF=""
if [ $ENABLE_JMX_REMOTE = true ]; then
	JMX_CONF="$JMX_CONF -Dcom.sun.management.jmxremote.port=$JMX_REMOTE_PORT -Dcom.sun.management.jmxremote.rmi.port=$JMX_REMOTE_RMI_PORT -Dcom.sun.management.jmxremote.authenticate=$ENABLE_JMX_REMOTE_AUTHENTICATION -Dcom.sun.management.jmxremote.ssl=$ENABLE_JMX_REMOTE_SSL"
	
	if [ ! -z $JMX_RMI_HOSTNAME ]; then
		JMX_CONF="$JMX_CONF -Djava.rmi.server.hostname=$JMX_RMI_HOSTNAME"
	fi

	if [ $ENABLE_JMX_REMOTE_AUTHENTICATION = true ]; then
		JMX_SECURITY_CONF="-Dcom.sun.management.jmxremote.access.file=$JMX_ACCESS_FILE -Dcom.sun.management.jmxremote.password.file=$JMX_PASSWORD_FILE"
	fi
fi
if [ $ENABLE_JMX_REMOTE_SSL = true ]; then
	JMX_SECURITY_CONF="$JMX_SECURITY_CONF -Djavax.net.ssl.keyStore=$SYNC_KEYSTORE -Djavax.net.ssl.keyStorePassword=$SYNC_KEYSTORE_PASSWORD -Djavax.net.ssl.keyStoreType=$SYNC_KEYSTORE_TYPE -Djavax.net.ssl.trustStore=$SYNC_TRUSTSTORE -Djavax.net.ssl.trustStoreType=$SYNC_TRUSTSTORE_TYPE -Djavax.net.ssl.trustStorePassword=$SYNC_TRUSTSTORE_PASSWORD"
fi
JMX_CONF="$JMX_CONF $JMX_SECURITY_CONF"

PGREP_STRING="$SYNC_JAR_FILE"
SUPPRESS_OUTPUT_CMD="> /dev/null 2>&1"

if [ $SYNC_VERBOSE_OUTPUT = true ]; then
SUPPRESS_OUTPUT_CMD="";
fi

START_CMD="cd $JAR_LOCATION;$JAVA_HOME/bin/java $JMX_CONF $JAVA_OPTS -cp $DB_CONNECTORS_FOLDER/*:$SYNC_JAR_FILE org.alfresco.service.sync.dropwizard.SyncService server $SYNC_JAR_CONFIG_YML_LOCATION  $SUPPRESS_OUTPUT_CMD &"
STOP_CMD="cd $JAR_LOCATION;$JAVA_HOME/bin/java $JMX_SECURITY_CONF $JAVA_OPTS -cp $SYNC_JAR_FILE org.alfresco.service.sync.SyncServiceShutdown --stop $SUPPRESS_OUTPUT_CMD"

CUR_USER=$(whoami)


#Extract the PID of the JAVA process running Sync service. 
#The JAVA process may be spawned from the process executing the 'sh' command, which also matches the filter. 
#Hence we just want the newest process in the chain, using the -n flag.
PID_GREP_CMD="\$(pgrep -u \$USER -f \${PGREP_STRING} -n)"

invoke_jar() {
	eval "$1"
}

log_success_msg() {
	echo "$*"
	logger "$_"
}

log_failure_msg() {
	echo "$*"
	logger "$_"
}

check_proc() {
	eval RET="$PID_GREP_CMD"
	if [ -n "$RET" ]; then
		return 0
	else
		return 1
	fi
}

start_script() {

	check_proc
	if [ $? -eq 0 ]; then
		eval PID="$PID_GREP_CMD"
		log_success_msg "$NAME with pid '$PID' is already running."
		exit 0
	fi
	
    #Make $USER the owner of the jxm password file
	if [ $ENABLE_JMX_REMOTE_AUTHENTICATION = true ]; then
		chown $USER: $JMX_PASSWORD_FILE
		chmod 600 $JMX_PASSWORD_FILE
	fi
	
	#Make $USER the owner of the log file
	SYNC_LOG_FILE=$SYNC_LOG_LOCATION/sync-service.log
	if [ -f $SYNC_LOG_FILE ]; then
		chown $USER: $SYNC_LOG_FILE
	fi

	invoke_jar "$START_CMD"
	# Sleep for a while to see if anything cries
	sleep 5

	check_proc
	if [ $? -eq 0 ]; then
		eval PID="$PID_GREP_CMD"
		log_success_msg "Started $NAME with pid $PID."
		echo $PID >"${PID_FILE}"
	else
		log_failure_msg "Error starting $NAME."
		exit 1
	fi
}

stop_script() {
	# if [ "${CUR_USER}" != "root" ]; then
	# 	log_failure_msg "You do not have permission to stop $NAME."
	# 	exit 1
	# fi

	eval PID="$PID_GREP_CMD"
	
	check_proc
	if [ $? -eq 0 ]; then
		echo "Invoking Sync service stop method."
		invoke_jar "\"$STOP_CMD $PID\""

		STOPPED="0"
		KILL_MAXSECONDS=15
		i=0
		echo "Waiting at most $KILL_MAXSECONDS seconds for regular termination of $NAME with pid: $PID."
		while [ "$i" -le "$KILL_MAXSECONDS" ]; do
			check_proc
			if [ $? -eq 0 ]; then
				sleep 1
				printf "."
				check_proc
			else
				STOPPED="1"
				break
			fi
			i="$(expr $i + 1)"
		done

		if [ "$STOPPED" -ne "1" ]; then
			log_failure_msg "Regular shutdown was not successful. Sending SIGKILL to process."
			kill -KILL $PID
			check_proc
			if [ $? -eq 0 ]; then
				log_failure_msg "Error stopping $NAME with pid: $PID."
				exit 1
			else
				log_success_msg "Stopped $NAME."
			fi
		else
			log_success_msg "Stopped $NAME."
		fi
	else
		log_failure_msg "$NAME is not running."
		exit 0
	fi
	rm -f "$PID_FILE" >/dev/null 2>&1
}

check_status() {
	check_proc
	if [ $? -eq 0 ]; then
		log_success_msg "$NAME is running."
	else
		log_failure_msg "$NAME is stopped."
		exit 1
	fi
}

case "$1" in
start)
	start_script
	;;
stop)
	stop_script
	;;
restart)
	stop_script
	start_script
	;;
status)
	check_status
	;;
*)
	echo "Usage: $0 {start|stop|restart|status}"
	exit 1
	;;
esac

exit 0
