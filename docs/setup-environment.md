# Setup Environment

This page describes how to setup an environment to test the ACS playbook.

For convenience this project makes use of _molecule_ to create and destroy, when testing on remote hosts, EC2 instances that are used as hosts. 

Molecule project is designed to aid in the development and testing of Ansible roles.  

Molecule provides support for testing with multiple instances, operating systems and distributions, virtualization providers, test frameworks and testing scenarios.  

NOTE: This page is for internal use only

[Prerequisites](#prereq)   
[Single Machine](#single)  
[Multi Machine](#multi) 

## <a name="prereq">Prerequisites

* Centos 7 EC2 instance using AMI from Marketplace
* Install Python3: 
```
sudo yum install -y python3-pip
```
* Install ansible, molecule and molecule-ec2, pyyaml: 
```
sudo pip3 install ansible==2.9.13 molecule==3.0.8 molecule-ec2==0.2 pyyaml
```
* Install Git
* Clone the project: 
```
  git clone https://github.com/Alfresco/alfresco-ansible-deployment.git
```  
* ```cd alfresco-ansible-deployment```
* ```export TRAVIS_BUILD_NUMBER```
* ```export TRAVIS_BRANCH```
* ```export AWS_ACCESS_KEY_ID```
* ```export AWS_SECRET_ACCESS_KEY```
* ```export AWS_DEFAULT_REGION```
* ```export NEXUS_USERNAME```
* ```export NEXUS_PASSWORD```


## <a name="single">Single Machine
To quickly provision a single machine deployment you need to follow these steps.  

```bash
export MOLECULE_EPHEMERAL_DIRECTORY=/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2
```
> This command will produce one EC2 instance.  
```bash
molecule create -s ec2
```

This command will display something similar in the terminal  

```bash
TASK [Wait for SSH] ************************************************************
    ok: [localhost] => (item={'address': 'EC2_IP_ADDRESS', 'identity_file': '/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2/', 'instance': 'EC2_INSTANCE_NAME', 'instance_ids': ['EC2_INSTANCE_ID'], 'port': 22, 'user': 'centos'})

    TASK [Wait for boot process to finish] *****************************************
    Pausing for 120 seconds
    (ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
    ok: [localhost]

    PLAY RECAP *********************************************************************
    localhost                  : ok=14   changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The create command produces the _instance_config.yml_ file in the MOLECULE_EPHEMERAL_DIRECTORY. This file contains information about the newly created EC2 instance (address, ssh key location, etc.). This information will be used to update the _inventory.yml_ file. For convenience a python script has been created (dynamic_inventory.py) to update the inventory file.

```bash
python3 molecule/ec2/dynamic_inventory.py
```

If you want to check that the EC2 instance is up and running, you can  _ping_ the host:

```bash
ansible all -m ping -i inventory.yml
```

To run the playbook just run:

```bash
ansible-playbook playbooks/acs.yml -i inventory.yml
```

Ansible will display play recap to let you know that everything is done, similar to the block below

 
```bash  
PLAY RECAP *****************************************************************************************************************************************************************
activemq_1                 : ok=24   changed=0    unreachable=0    failed=0    skipped=17   rescued=0    ignored=0
adw_1                      : ok=24   changed=6    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0
database_1                 : ok=20   changed=0    unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
nginx_1                    : ok=21   changed=8    unreachable=0    failed=0    skipped=8    rescued=0    ignored=0
repository_1               : ok=92   changed=43   unreachable=0    failed=0    skipped=14   rescued=0    ignored=0
search_1                   : ok=34   changed=13   unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
syncservice_1              : ok=39   changed=18   unreachable=0    failed=0    skipped=13   rescued=0    ignored=0
transformers_1             : ok=81   changed=10   unreachable=0    failed=0    skipped=44   rescued=0    ignored=0
```

To delete the EC2 instance:  
```bash
molecule destroy -s ec2
```

## <a name="multi">Multi Machine

To quickly provision a multi machine deployment you need to follow these steps.  

```bash
export MOLECULE_EPHEMERAL_DIRECTORY=/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2multi
```

> This command will produce 7 EC2 instances
```bash
molecule create -s ec2multi
```

This command will display something similar in the terminal. Full log not shown here for brevity.  

```bash
TASK [Wait for SSH] ************************************************************
    ok: [localhost] => (item={'address': 'EC2_IP_ADDRESS', 'identity_file': '/home/centos/.cache/molecule/alfresco-ansible-deployment/ec2/', 'instance': 'EC2_INSTANCE_NAME', 'instance_ids': ['EC2_INSTANCE_ID'], 'port': 22, 'user': 'centos'})

    TASK [Wait for boot process to finish] *****************************************
    Pausing for 120 seconds
    (ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
    ok: [localhost]

    PLAY RECAP *********************************************************************
    localhost                  : ok=14   changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The create command produces the _instance_config.yml_ file in the MOLECULE_EPHEMERAL_DIRECTORY. This file contains information about the newly created EC2 instances (address, ssh key location, etc.). This information will be used to update the _inventory.yml_ file. For convenience a python script has been created (dynamic_inventory.py) to update the inventory file.

```bash
python3 molecule/ec2multi/dynamic_inventory.py
```

If you want to check that the EC2 instances are up and running, you can  _ping_ the hosts:

```bash
ansible all -m ping -i inventory.yml
```

To run the playbook just run:

```bash
ansible-playbook playbooks/acs.yml -i inventory.yml
```

Ansible will display play recap to let you know that everything is done, similar to the block below

 
```bash  
PLAY RECAP *****************************************************************************************************************************************************************
activemq_1                 : ok=24   changed=0    unreachable=0    failed=0    skipped=17   rescued=0    ignored=0
adw_1                      : ok=24   changed=6    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0
database_1                 : ok=20   changed=0    unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
nginx_1                    : ok=21   changed=8    unreachable=0    failed=0    skipped=8    rescued=0    ignored=0
repository_1               : ok=92   changed=43   unreachable=0    failed=0    skipped=14   rescued=0    ignored=0
search_1                   : ok=34   changed=13   unreachable=0    failed=0    skipped=11   rescued=0    ignored=0
syncservice_1              : ok=39   changed=18   unreachable=0    failed=0    skipped=13   rescued=0    ignored=0
transformers_1             : ok=81   changed=10   unreachable=0    failed=0    skipped=44   rescued=0    ignored=0
```

To delete the EC2 instances:  
```bash
molecule destroy -s ec2multi
```