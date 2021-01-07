#!/bin/bash

wget -qO /dev/null --user=${NEXUS_USERNAME} --password=${NEXUS_PASSWORD} https://artifacts.alfresco.com/nexus/service/local/repositories/activiti-enterprise-releases/content/com/activiti/activiti-enterprise/1.9.0.6/activiti-enterprise-1.9.0.6.pom
if [ $? -ne 0 ]
    then
      echo "Nexus credentials not working, please set NEXUS_USERNAME and NEXUS_PASSWORD as specified in the deployment guide"
      echo "export NEXUS_USERNAME=\"<your-username>\""
      echo "export NEXUS_PASSWORD=\"<your-password>\""
    else
      echo "Nexus credentials are working"
      echo "Testing Local Inventory files next:..."
      ansible all -m ping -i ../inventory_local.yml
      if [ $? -ne 0 ]; then
        echo "Local inventory wrong"
      fi
      echo "Testing Ssh Inventory files next:..."
      ansible all -m ping -i ../inventory_ssh.yml
      if [ $? -ne 0 ]; then
        echo "Ssh inventory wrong"
      fi
fi
