#!/bin/bash -e

AMI_ID=$1
EXTRA_VARS_FILE=$2
TEST_CONFIG_FILE=$3
FLAVOUR=$4
TEST_ID="${TRAVIS_BRANCH}_${TRAVIS_BUILD_NUMBER}_$4"

function cleanup {
  echo "Destroying $INSTANCE_ID"
  aws ec2 terminate-instances --instance-ids $INSTANCE_ID
}

trap cleanup EXIT

openssl aes-256-cbc -K $encrypted_6c8b9ee48a27_key -iv $encrypted_6c8b9ee48a27_iv \
    -in alfresco-ansible.pem.enc -out /tmp/dbp-ansible -d

eval "$(ssh-agent -s)"
chmod 600 /tmp/dbp-ansible
ssh-add /tmp/dbp-ansible

curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
./awscli-bundle/install -b ~/bin/aws
PATH=~/bin:$PATH
export AWS_DEFAULT_REGION='us-east-1'

git clone --depth 1 --branch $DTAS_VERSION https://$GITHUB_TOKEN@github.com/Alfresco/alfresco-deployment-test-automation-scripts.git dtas

aws ec2 run-instances --image-id $AMI_ID \
    --count 1 --instance-type t3.large --key-name dbp-ansible \
    --security-group-ids sg-099a05787b0a322c3 --subnet-id subnet-06ffe524598660d99 \
    --tag-specifications "ResourceType=instance,Tags=[{Key=local,Value=${TEST_ID}},{Key=Creator,Value=${TEST_ID}},{Key=Owner,Value="Operator\ Experience\ Team"},{Key=Department,Value=Engineering},{Key=Purpose,Value=${TEST_ID}},{Key=NoAutomaticShutdown,Value=false},{Key=Production,Value=False},{Key=Name,Value=molecule_${TEST_ID}},{Key=instance,Value=${TEST_ID}}]"

echo "wait for instance to be up" && sleep 4m

PUBLIC_IP=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=running Name=tag-key,Values=local Name=tag-value,Values=${TEST_ID} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text)
INSTANCE_ID=$(aws ec2 describe-instances --filters Name=tag-key,Values=local Name=tag-value,Values=$TEST_ID --query 'Reservations[*].Instances[*].InstanceId' --output text)

echo "$INSTANCE_ID created"

ssh-keyscan $PUBLIC_IP >> ~/.ssh/known_hosts

./scripts/generate-zip.sh
VERSION=$(cat ./VERSION)

if [[ $FLAVOUR == centos* ]]; then
  SSH_CONNECTION_STRING=centos@${PUBLIC_IP}
  SSH_HOME="/home/centos"
  INSTALL_DEPENDENCIES="sudo yum install -y -q unzip python3 && sudo pip3 install virtualenv"
elif [[ $FLAVOUR == ubuntu* ]]; then
  SSH_CONNECTION_STRING=ubuntu@${PUBLIC_IP}
  SSH_HOME="/home/ubuntu"
  INSTALL_DEPENDENCIES="sudo apt-get update -q && sudo apt-get install -qy unzip python3 virtualenvwrapper"
else
  echo "${FLAVOUR} not supported"
  exit 1
fi

scp "./dist/alfresco-ansible-deployment-${VERSION}.zip" "${SSH_CONNECTION_STRING}:${SSH_HOME}/"
ssh "${SSH_CONNECTION_STRING}" "${INSTALL_DEPENDENCIES}"
ssh "${SSH_CONNECTION_STRING}" "mkdir ~/.pythonvenv && virtualenv -p /usr/bin/python3 ~/.pythonvenv/ansible-${ANSIBLE_VERSION}"
ssh "${SSH_CONNECTION_STRING}" "source ~/.pythonvenv/ansible-${ANSIBLE_VERSION}/bin/activate && pip install --upgrade pip && pip install ansible==${ANSIBLE_VERSION}"
ssh "${SSH_CONNECTION_STRING}" "unzip alfresco-ansible-deployment-${VERSION}.zip"
scp -r tests "${SSH_CONNECTION_STRING}:${SSH_HOME}/alfresco-ansible-deployment-${VERSION}/"
ssh ${SSH_CONNECTION_STRING} "export NEXUS_USERNAME=\"$NEXUS_USERNAME\"; export NEXUS_PASSWORD=\"$NEXUS_PASSWORD\"; cd alfresco-ansible-deployment-${VERSION}; source ~/.pythonvenv/ansible-${ANSIBLE_VERSION}/bin/activate && ansible-playbook playbooks/acs.yml -i inventory_local.yml -e \"@${EXTRA_VARS_FILE}\""

sed -i "s+TEST_URL+http://${PUBLIC_IP}+g" "tests/$TEST_CONFIG_FILE"
cd dtas
pytest --tb=line --configuration "../tests/${TEST_CONFIG_FILE}" tests/ -s

if [[ "$TRAVIS_COMMIT_MESSAGE" != *"[keep env]"* ]]; then exit 0; fi
aws ec2 terminate-instances --instance-ids "${INSTANCE_ID}"