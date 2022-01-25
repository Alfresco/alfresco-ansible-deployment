#!/bin/bash -e
aws ec2 run-instances --image-id ami-0affd4508a5d2481b \
    --count 1 --instance-type t3.large --key-name dbp-ansible \
    --security-group-ids sg-099a05787b0a322c3 --subnet-id subnet-06ffe524598660d99 \
    --tag-specifications "ResourceType=instance,Tags=[{Key=local,Value=machine_no_${TRAVIS_BUILD_NUMBER}},{Key=Creator,Value=${TRAVIS_BUILD_NUMBER}_${TRAVIS_BUILD_NUMBER}},{Key=Owner,Value="Operator\ Experience\ Team"},{Key=Department,Value=Engineering},{Key=Purpose,Value=${TRAVIS_BUILD_NUMBER}_${TRAVIS_BUILD_NUMBER}_local},{Key=NoAutomaticShutdown,Value=false},{Key=Production,Value=False},{Key=Name,Value=molecule_${TRAVIS_BRANCH}_${TRAVIS_BUILD_NUMBER}_local},{Key=instance,Value=${TRAVIS_BRANCH}_${TRAVIS_BUILD_NUMBER}_local}]"

echo "wait for instance to be up" && sleep 4m

export PUBLIC_IP=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=running Name=tag-key,Values=local Name=tag-value,Values=machine_no_${TRAVIS_BUILD_NUMBER} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text)
export INSTANCE_ID=$(aws ec2 describe-instances --filters Name=tag-key,Values=local Name=tag-value,Values=machine_no_${TRAVIS_BUILD_NUMBER} --query 'Reservations[*].Instances[*].InstanceId' --output text)

ssh-keyscan $PUBLIC_IP >> ~/.ssh/known_hosts

scripts/generate-zip.sh
export VERSION=$(cat VERSION)
scp dist/alfresco-ansible-deployment-${VERSION}.zip centos@${PUBLIC_IP}:/home/centos/
ssh centos@${PUBLIC_IP} "sudo yum install -y -q unzip python3 python-virtualenv"
ssh centos@${PUBLIC_IP} "mkdir ~/.pythonvenv && virtualenv -p /usr/bin/python3 ~/.pythonvenv/ansible-${ANSIBLE_VERSION}"
ssh centos@${PUBLIC_IP} "source ~/.pythonvenv/ansible-${ANSIBLE_VERSION}/bin/activate && pip install --upgrade pip && pip install ansible==${ANSIBLE_VERSION}"
ssh centos@${PUBLIC_IP} "unzip alfresco-ansible-deployment-${VERSION}.zip"
scp -r tests centos@${PUBLIC_IP}:/home/centos/alfresco-ansible-deployment-${VERSION}/
ssh centos@${PUBLIC_IP} "export NEXUS_USERNAME=$NEXUS_USERNAME; export NEXUS_PASSWORD=\"$NEXUS_PASSWORD\"; cd alfresco-ansible-deployment-${VERSION}; source ~/.pythonvenv/ansible-${ANSIBLE_VERSION}/bin/activate && ansible-playbook playbooks/acs.yml -i inventory_local.yml -e \"@6.2.N-extra-vars.yml\""

sed -i "s+TEST_URL+http://$PUBLIC_IP+g" "tests/test-config-acs6-stack.json" 
cd dtas
pytest --tb=line --configuration ../tests/test-config-acs6-stack.json tests/ -s
if [[ "$TRAVIS_COMMIT_MESSAGE" == *"[keep env]"* ]]; then exit 0; fi
aws ec2 terminate-instances --instance-ids $INSTANCE_ID