from datetime import datetime, timedelta
import logging
from dateutil import parser
import botocore
import boto3

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)
_region = 'us-east-1'
_ec2 = boto3.client('ec2', region_name=_region)
_ec2_resource = boto3.resource('ec2')
_filters = [
    {
        'Name': 'tag:Name',
        'Values': ['molecule_OPSEXP*', 'molecule_master_*']
    },
    {
        'Name':'tag:NoAutomaticShutdown',
        'Values': ['false']
    },
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
        ]

def lambda_handler(event, context):
    """ Lambda Handler """

    response = _ec2.describe_instances(Filters=_filters)
    instances_to_terminate = _get_instances_to_terminate(response)
    if len(instances_to_terminate) > 0:
        for instance in instances_to_terminate:
            _ec2.terminate_instances(InstanceIds=[instance['InstanceId']])
            _logger.info('Terminated the following instance: %s', str(instance['InstanceId']))
            if instance['KeyName'] != "dbp-ansible":
                try:
                    _boto_instance = _ec2_resource.Instance(instance['InstanceId'])
                    _boto_instance.modify_attribute(Groups=['sg-c40c148f']) #Added here the default vpc sg since this list cant be passed empty
                    _logger.info('Reassigned the security group for instance: %s', str(instance['InstanceId']))
                    _ec2.delete_security_group(GroupId=instance['GroupId'])
                    _logger.info('Deleted the following security group: %s', str(instance['GroupId']))
                except botocore.exceptions.ClientError as error:
                    if error.response['Error']['Code'] == 'DependencyViolation':
                        _logger.warn('SG %s has a dependent object...',instance['GroupId'])
                    else:
                        raise error
                _ec2.delete_key_pair(KeyName=instance['KeyName'])
                _logger.info('Deleted the following key pair: %s', str(instance['KeyName']))
    else:
        _logger.info('No instances to terminate')

def _get_instances_to_terminate(response):
    """ Getting instances that need to be cleaned up"""

    instances_to_terminate = []
    if 'Reservations' in response and len(response['Reservations']) > 0:
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                launchTime = parser.parse(str(instance['LaunchTime'])).replace(tzinfo=None)
                time_to_delete = datetime.now() + timedelta(days = -1)
                if launchTime < time_to_delete:
                    _logger.info(str({'InstanceId': instance['InstanceId'], 'KeyName': instance['KeyName'], 'GroupId': instance['SecurityGroups'][0]['GroupId']}))
                    _logger.info('Add ec2 instance Id to terminate list: %s', instance['InstanceId'])
                    instances_to_terminate.append({'InstanceId': instance['InstanceId'], 'KeyName': instance['KeyName'], 'GroupId': instance['SecurityGroups'][0]['GroupId']})
    return instances_to_terminate
