import boto3
import json

def lambda_handler(event, context):
    ec2_resource = boto3.resource('ec2', 'us-east-1')
    filter = {"Name":"tag:Name", "Values":["enesai"]}
    for each_ec2 in ec2_resource.instances.filter(Filters=[filter]):
        each_ec2.start()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello form Lambda!')
    }