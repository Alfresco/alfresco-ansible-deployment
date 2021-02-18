import logging
from datetime import datetime, timedelta
from dateutil import parser
import boto3

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)
_ec2 = boto3.client('ec2')
_filters = [
    {
        'Name': 'tag:Name',
        'Values': ['molecule_OPSEXP-*', 'molecule_master_*']
    },
    {
        'Name':'tag:NoAutomaticShutdown',
        'Values': ['false']
    },
    {
        'Name': 'instance-state-name',
        'Values': ['running','stopped']
    }
]
_sg_filters = [{ 'Name': 'group-name', 'Values': ['molecule_OPSEXP-*', 'molecule_master_*']}]
_key_filters = [{ 'Name': 'key-name', 'Values': ['molecule_OPSEXP-*', 'molecule_master_*']}]

def lambda_handler(event, context):
    """Lambda entry point"""

    response = _ec2.describe_instances(Filters=_filters)
    instances_to_terminate = _get_instances_to_terminate(response)
    if len(instances_to_terminate) > 0:
        _ec2.terminate_instances(InstanceIds=instances_to_terminate)
        _logger.info('Terminated the following instances: %s', str(instances_to_terminate))
    else:
        _logger.info('No instances to terminate')

    sgs = _ec2.describe_security_groups(Filters=_sg_filters)
    sgs_to_terminate = _get_sgs_to_delete(sgs['SecurityGroups'])
    if len(sgs_to_terminate) > 0:
        for sg in sgs_to_terminate:
            _ec2.delete_security_group(GroupId=sg)
            _logger.info('Deleted the following security group: ' + str(sg))
    else:
        _logger.info('No security groups to delete')

    keys = _ec2.describe_key_pairs(Filters=_key_filters)
    keys_to_terminate = _get_keys_to_delete(keys['KeyPairs'])
    if len(keys_to_terminate) > 0:
        for key in keys_to_terminate:
            _ec2.delete_key_pair(KeyPairId=key)
            _logger.info('Deleted the following key pair: ' + str(sg))
    else:
        _logger.info('No key pair to delete')

def _get_instances_to_terminate(response):
    """Build list of instance IDs to terminate"""

    instances_to_terminate = []
    if 'Reservations' in response and len(response['Reservations']) > 0:
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                launchTime = parser.parse(str(instance['LaunchTime'])).replace(tzinfo=None)
                time_to_delete = datetime.now() + timedelta(days = -1)
                if launchTime < time_to_delete:
                    instance_to_terminate = instance['InstanceId']
                    _logger.info('Add ec2 instance Id to terminate list: %s', instance_to_terminate)
                    instances_to_terminate.append(instance_to_terminate)
    return instances_to_terminate

def _get_sgs_to_delete(response):
    """Build list of security group IDs to delete"""

    sgs_to_terminate = []
    for sgs in response:
        sgs_to_terminate.append(sgs['GroupId'])
    return sgs_to_terminate
    
def _get_keys_to_delete(response):
    """Build list of key pair IDs to delete"""

    keys_to_terminate = []
    for key in response:
        keys_to_terminate.append(key['KeyPairId'])
    return keys_to_terminate
