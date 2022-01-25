#!/bin/bash -e

AMI_ID=$1
EXTRA_VARS_FILE=$2
TEST_CONFIG_FILE=$3
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

export PATH=~/bin:$PATH
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export AWS_DEFAULT_REGION='us-east-1'

git clone --depth 1 --branch $DTAS_VERSION https://$GITHUB_TOKEN@github.com/Alfresco/alfresco-deployment-test-automation-scripts.git dtas

aws ec2 run-instances --image-id $AMI_ID \
    --count 1 --instance-type t3.large --key-name dbp-ansible \
    --security-group-ids sg-099a05787b0a322c3 --subnet-id subnet-06ffe524598660d99 \
    --tag-specifications "ResourceType=instance,Tags=[{Key=local,Value=${TEST_ID}},{Key=Creator,Value=${TEST_ID}},{Key=Owner,Value="Operator\ Experience\ Team"},{Key=Department,Value=Engineering},{Key=Purpose,Value=${TEST_ID}},{Key=NoAutomaticShutdown,Value=false},{Key=Production,Value=False},{Key=Name,Value=molecule_${TEST_ID}},{Key=instance,Value=${TEST_ID}}]"

echo "wait for instance to be up" && sleep 4m

export PUBLIC_IP=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=running Name=tag-key,Values=local Name=tag-value,Values=${TEST_ID} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text)
export INSTANCE_ID=$(aws ec2 describe-instances --filters Name=tag-key,Values=local Name=tag-value,Values=$TEST_ID --query 'Reservations[*].Instances[*].InstanceId' --output text)

echo "$INSTANCE_ID created"

ssh-keyscan $PUBLIC_IP >> ~/.ssh/known_hosts

./scripts/generate-zip.sh
export VERSION=$(cat VERSION)
scp ./dist/alfresco-ansible-deployment-${VERSION}.zip centos@${PUBLIC_IP}:/home/centos/
ssh centos@${PUBLIC_IP} "sudo yum install -y -q unzip python3 python-virtualenv"
ssh centos@${PUBLIC_IP} "mkdir ~/.pythonvenv && virtualenv -p /usr/bin/python3 ~/.pythonvenv/ansible-${ANSIBLE_VERSION}"
ssh centos@${PUBLIC_IP} "source ~/.pythonvenv/ansible-${ANSIBLE_VERSION}/bin/activate && pip install --upgrade pip && pip install ansible==${ANSIBLE_VERSION}"
ssh centos@${PUBLIC_IP} "unzip alfresco-ansible-deployment-${VERSION}.zip"
scp -r tests centos@${PUBLIC_IP}:/home/centos/alfresco-ansible-deployment-${VERSION}/
ssh centos@${PUBLIC_IP} "export NEXUS_USERNAME=$NEXUS_USERNAME; export NEXUS_PASSWORD=\"$NEXUS_PASSWORD\"; cd alfresco-ansible-deployment-${VERSION}; source ~/.pythonvenv/ansible-${ANSIBLE_VERSION}/bin/activate && ansible-playbook playbooks/acs.yml -i inventory_local.yml -e \"@${EXTRA_VARS_FILE}\""

sed -i "s+TEST_URL+http://$PUBLIC_IP+g" "tests/${TEST_CONFIG_FILE}"
cd dtas
pytest --tb=line --configuration ../tests/${TEST_CONFIG_FILE} tests/ -s
if [[ "$TRAVIS_COMMIT_MESSAGE" == *"[keep env]"* ]]; then exit 0; fi
aws ec2 terminate-instances --instance-ids $INSTANCE_ID