import logging
import boto3
from datetime import datetime, timedelta
from dateutil import parser

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

def lambda_handler(event, context):
    response = _ec2.describe_instances(Filters=_filters)
    instances_to_terminate = _get_instances_to_terminate(response)
    
    if len(instances_to_terminate) > 0:
        _ec2.terminate_instances(InstanceIds=instances_to_terminate)
        _logger.info('Terminated the following instances: ' + str(instances_to_terminate))
    else:
        _logger.info('No instances to terminate')
    
def _get_instances_to_terminate(response):
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