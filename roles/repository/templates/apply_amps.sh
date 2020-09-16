#!/bin/sh
. /etc/opt/alfresco/setenv.sh

echo "Installing Content Services Platform AMPs ..."
sudo ${JAVA_HOME}/bin/java -jar ${ACS_HOME}/bin/alfresco-mmt.jar install /opt/alfresco/modules/acs-platform ${ACS_HOME}/web-server/webapps/alfresco.war -directory $*
sudo ${JAVA_HOME}/bin/java -jar ${ACS_HOME}/bin/alfresco-mmt.jar install ${ACS_HOME}/amps ${ACS_HOME}/web-server/webapps/alfresco.war -directory -nobackup $*
sudo ${JAVA_HOME}/bin/java -jar ${ACS_HOME}/bin/alfresco-mmt.jar list ${ACS_HOME}/web-server/webapps/alfresco.war

echo "Installing Content Services Share AMPs ..."
sudo ${JAVA_HOME}/bin/java -jar ${ACS_HOME}/bin/alfresco-mmt.jar install /opt/alfresco/modules/acs-share ${ACS_HOME}/web-server/webapps/share.war -directory $*
if [ -d ${ACS_HOME}/amps_share ]; then
    sudo ${JAVA_HOME}/bin/java -jar ${ACS_HOME}/bin/alfresco-mmt.jar install ${ACS_HOME}/amps_share ${ACS_HOME}/web-server/webapps/share.war -directory -nobackup $*
fi
sudo ${JAVA_HOME}/bin/java -jar ${ACS_HOME}/bin/alfresco-mmt.jar list ${ACS_HOME}/web-server/webapps/share.war

echo "Clearing Tomcat Application Cache ..."
sudo rm -rf ${ACS_HOME}/web-server/webapps/alfresco
sudo rm -rf ${ACS_HOME}/web-server/webapps/share