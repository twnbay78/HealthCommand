import json
import boto3
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel('INFO')
rds = boto3.client('rds')

def start_db_instance(db_instance_identifier):
    instance_description = rds.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
    logger.info('instance_descriptipn_response: {instance_description}'.format(instance_description = instance_description))
    if 'DBInstances' in instance_description and len(instance_description['DBInstances']) == 1:
        if instance_description['DBInstances'][0]['DBInstanceStatns'] == 'available':
            logger.info('healthcommand instance already started, skipping...')
        else:
            start_instance_response = rds.start_db_instance(DBInstanceIdentifier='healthcommand')
            logger.info('start_instance_response: {start_instance_response}'.format(start_instance_response = start_instance_response))

def stop_db_instance(db_instance_identifier):
    instance_description = rds.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
    logger.info('instance_descriptipn_response: {instance_description}'.format(instance_description = instance_description))
    if 'DBInstances' in instance_description and len(instance_description['DBInstances']) == 1:
        if instance_description['DBInstances'][0]['DBInstanceStatus'] != 'available':
            logger.info('healthcommand instance already inactive, skipping...')
        else:
            start_instance_response = rds.stop_db_instance(DBInstanceIdentifier='healthcommand')
            logger.info('start_instance_response: {start_instance_response}'.format(start_instance_response = start_instance_response))


'''
TODO:
- Include webserver and backend server
'''
def lambda_handler(event, context):
    logger.info('context: {context}'.format(context = context, event = event))
    logger.info('event: {event}'.format(event = event))
    if event['action'].lower() == 'start':
        start_db_instance('healthcommand')

    elif event['action'].lower() == 'stop':
        stop_db_instance('healthcommand')
    
    else: 
        logger.error('Unexpected input, please ensure the "action" key is included within the request body and has either a value of "start" or "stop"')
        return {
            'statusCode': 400,
            'body': json.dumps('Instance start/shutdown service unsuccessful'),
            'headers': {'request_id': context.aws_request_id}
        }

            
    return {
        'statusCode': 200,
        'body': json.dumps('Instance start/shutdown service successful'),
        'headers': {'request_id': context.aws_request_id}
    }
