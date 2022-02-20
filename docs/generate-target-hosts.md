# Generate Target Hosts

This page describes how to generate one or more target hosts and an inventory file that can be used to test the ACS playbook.

Until we have a more convenient mechanism to create test machines i.e. Terraform or CloudFormation we can use `molecule`, a tool designed for testing Ansible playbooks.

Molecule provides support for testing with multiple instances, operating systems and distributions, virtualization providers, test frameworks and testing scenarios. It also provides a way to create and destroy AWS EC2 instances that can be used as target hosts, we use this as part of our internal testing pipeline.

## Prerequisites

1. The ID of an AWS VPC subnet to deploy to
2. You have followed the steps in the [Setup A Control Node](./deployment-guide.md#setup-a-control-node) section
3. Install Python3 on the control node

    ```bash
    sudo yum install -y python3-pip
    ```

4. Install ansible, molecule and molecule-ec2, pyyaml on the control node

    ```bash
    sudo pip3 install ansible==2.9.18 molecule==3.0.8 molecule-ec2==0.2 pyyaml
    ```

5. As the scripts are designed to work in our build environment a `TRAVIS_BUILD_NUMBER` and `TRAVIS_BRANCH` environment variable is expected. These can be set to whatever you want, they are used to name the EC2 instances.

    ```bash
    export TRAVIS_BUILD_NUMBER=1
    export TRAVIS_BRANCH=test
    ```

6. Molecule needs AWS credentials to create the key pairs, security group and EC2 machines

    ```bash
    export AWS_ACCESS_KEY_ID=<your-key-id>
    export AWS_SECRET_ACCESS_KEY=<your-access-key>
    export AWS_DEFAULT_REGION=<your-region>
    ```

## Generate Single Target Host

To quickly provision a single target host follow the steps below.

1. Make sure you are in the root of the cloned repository i.e. in the `alfresco-ansible-deployment` folder

2. Update the `vpc_subnet_id` value in molecule/ec2/molecule.yml for your environment

    NOTE: If you want to use a region other than us-east-1 you'll also need to update the AMI ID value

3. Run molecule to create the infrastructure

    ```bash
    molecule create -s ec2
    ```

    Once complete you will see ouptut similar to that shown below:

    > TASK [Wait for SSH] **********************************************************
    > ok: [localhost] => (item={'address': 'EC2_IP_ADDRESS', 'identity_file': '/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2/ssh_key', 'instance': 'EC2_INSTANCE_NAME', 'instance_ids': ['EC2_INSTANCE_ID'], 'port': 22, 'user': 'centos'})
    >
    > TASK [Wait for boot process to finish] ***************************************
    > Pausing for 120 seconds
    > (ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
    > ok: [localhost]
    >
    > PLAY RECAP *******************************************************************
    > localhost                  : ok=14   changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

4. Create a `MOLECULE_EPHEMERAL_DIRECTORY` environment variable

    ```bash
    export MOLECULE_EPHEMERAL_DIRECTORY=/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2
    ```

5. The create command produces an `instance_config.yml` file in the `MOLECULE_EPHEMERAL_DIRECTORY`. This file contains information about the newly created EC2 instance (address, ssh key location, etc.). This information will be used to update the `inventory_ssh.yml` file. For convenience a python script, `dynamic_inventory.py`, has been created to update the inventory file.

    ```bash
    python3 molecule/ec2/dynamic_inventory.py
    ```

You are now ready to run the playbook, please return to the [deployment guide and follow the steps to deploy](./deployment-guide.md#single-machine-deployment).

## Generate Multiple Target Hosts

To quickly provision multiple target hosts follow the steps below.

1. Make sure you are in the root of the cloned repository i.e. in the `alfresco-ansible-deployment` folder

2. Update the `vpc_subnet_id` value in molecule/ec2multi/molecule.yml for your environment

    NOTE: If you want to use a region other than us-east-1 you'll also need to update the AMI ID value

3. Run molecule to create the infrastructure

    ```bash
    molecule create -s ec2multi
    ```

    Once complete you will see ouptut similar to that shown below:

    > TASK [Wait for SSH] **********************************************************
    > ok: [localhost] => (item={'address': 'EC2_IP_ADDRESS', 'identity_file': '/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2/ssh_key', 'instance': 'EC2_INSTANCE_NAME', 'instance_ids': ['EC2_INSTANCE_ID'], 'port': 22, 'user': 'centos'})
    >
    > TASK [Wait for boot process to finish] ***************************************
    > Pausing for 120 seconds
    > (ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
    > ok: [localhost]
    >
    > PLAY RECAP *******************************************************************
    > localhost                  : ok=14   changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

4. Create a `MOLECULE_EPHEMERAL_DIRECTORY` environment variable

    ```bash
    export MOLECULE_EPHEMERAL_DIRECTORY=/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2multi
    ```

5. The create command produces an `instance_config.yml` file in the `MOLECULE_EPHEMERAL_DIRECTORY`. This file contains information about the newly created EC2 instance (address, ssh key location, etc.). This information will be used to update the `inventory_ssh.yml` file. For convenience a python script, `dynamic_inventory.py`, has been created to update the inventory file.

    ```bash
    python3 molecule/ec2multi/dynamic_inventory.py
    ```

You are now ready to run the playbook, please return to the [deployment guide and follow the steps to deploy](./deployment-guide.md#multi-machine-deployment).

## Cleanup

Molecule can also be used to delete the resources we created by running `molecule destroy -s ec2` if you generated a single target host or `molecule destroy -s ec2multi` if you generated multiple target hosts.
