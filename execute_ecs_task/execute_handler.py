import logging

import boto3

logger = logging.getLogger()


def execute_ecs_event(event, context):
    """
    Event is an s3 trigger containing the taskdef ARN.

    Connect to an s3 bucket, download a certain key.

    Execute this ARN, and return a happy status or explode.
    :param event:
    :param context:
    :return:
    """
    logger.debug(f'got event: {event}')

    # look at event, get relevant s3 data
    # Note: in production you would typically make sure this lambda only reads
    # events from certain buckets, whitelisting the ARN
    # also only that bucket would have invoke permissions on this lambda
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        src_key = event['Records'][0]['s3']['object']['key']
    except (KeyError, IndexError):
        raise InvalidEventException("Must be a s3 trigger event")

    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket=bucket, Key=src_key)
    arn = obj['Body'].read()
    arn = arn.decode("utf-8")

    logger.info(f'got arn: {arn}')

    # execute arn
    # note: moto ECS currently only works in us-east-1, it seems.
    ecs_client = boto3.client('ecs', region_name='us-east-1')

    # the boto3 documentation lists quite a long list of params for this task
    # as I am unfamiliar with ecs, I'm only providing the required fields
    # in a real-world scenario, many of these parameters are optional but would be required
    # for an actual production lambda
    # http://boto3.readthedocs.io/en/latest/reference/services/ecs.html#ECS.Client.run_task
    # TODO: Moto has a bug around run_task https://github.com/spulec/moto/issues/1660
    response = ecs_client.run_task(taskDefinition=arn, cluster='test_ecs_cluster')

    # verify response
    if 'failures' in response and len(response['failures']) > 0:
        raise InvalidTaskExecutationState

    return response



class InvalidEventException(Exception):
    pass


class InvalidTaskExecutationState(Exception):
    pass
