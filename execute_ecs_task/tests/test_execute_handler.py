import json
import io
import boto3

from moto import mock_s3, mock_ecs, mock_ec2
from moto.ec2 import utils as ec2_utils
from execute_ecs_task.execute_handler import execute_ecs_event


@mock_s3
@mock_ecs
@mock_ec2
def test_ecs_run_task():
    """
    Save and return an object using the Helper function
    :return:
    """
    # client and setup mock bucket
    s3 = boto3.resource('s3', region_name='us-west-2')
    s3_client = boto3.client('s3')
    s3_bucket = "s3bucket"
    s3_key = "arnkey"
    s3.create_bucket(Bucket=s3_bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})

    # s3 needs a file-like object
    # moto is oddly specific in how it names this
    arn_io = io.BytesIO(b'arn:aws:ecs:us-east-1:012345678910:task-definition/test_ecs_task:1')

    # Upload the file to "S3"
    s3_client.upload_fileobj(arn_io, s3_bucket, s3_key)

    # This is an s3 PUT trigger event
    event = {
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "AIDAJDPLRKLG7UEXAMPLE"
                },
                "requestParameters": {
                    "sourceIPAddress": "127.0.0.1"
                },
                "responseElements": {
                    "x-amz-request-id": "C3D13FE58DE4C810",
                    "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "s3bucket",
                        "ownerIdentity": {
                            "principalId": "A3NL1KOZZKExample"
                        },
                        "arn": "arn:aws:s3:::mybucket"
                    },
                    "object": {
                        "key": "arnkey",
                        "size": 1024,
                        "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                        "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko",
                        "sequencer": "0055AED6DCD90281E5"
                    }
                }
            }
        ]
    }

    # setup ecs cluster
    # This setup lifted from https://github.com/spulec/moto/blob/master/tests/test_ecs/test_ecs_boto3.py
    ecs_client = boto3.client('ecs', region_name='us-east-1')
    ec2_client = boto3.resource('ec2', region_name='us-east-1')
    test_cluster_name = 'test_ecs_cluster'

    _ = ecs_client.create_cluster(
        clusterName=test_cluster_name
    )

    test_instance = ec2_client.create_instances(
        ImageId="ami-1234abcd",
        MinCount=1,
        MaxCount=1,
    )[0]

    instance_id_document = json.dumps(
        ec2_utils.generate_instance_identity_document(test_instance)
    )

    response = ecs_client.register_container_instance(
        cluster=test_cluster_name,
        instanceIdentityDocument=instance_id_document
    )

    _ = ecs_client.register_task_definition(
        family='test_ecs_task',
        containerDefinitions=[
            {
                'name': 'hello_world',
                'image': 'docker/hello-world:latest',
                'cpu': 1024,
                'memory': 400,
                'essential': True,
                'environment': [{
                    'name': 'AWS_ACCESS_KEY_ID',
                    'value': 'SOME_ACCESS_KEY'
                }],
                'logConfiguration': {'logDriver': 'json-file'}
            }
        ]
    )
    # response = ecs_client.run_task(
    #     cluster='test_ecs_cluster',
    #     overrides={},
    #     taskDefinition='test_ecs_task',
    #     count=2,
    #     startedBy='moto'
    # )

    response = execute_ecs_event(event, None)
    print(response)