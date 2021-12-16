import boto3

ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto')
client = ec2_console.client('ec2', region_name='us-east-1')

print('Creating EC2 instance')
response = client.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {

                'DeleteOnTermination': True,
                'VolumeSize': 8,
                'VolumeType': 'gp2'
            },
        },
    ],
    ImageId='ami-0ed9277fb7eb570c9',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    Monitoring={
        'Enabled': False
    },
    SecurityGroupIds=[
        'sg-0780abfac785fa066',
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'enesai'
                },
                {
                    'Key': 'env',
                    'Value': 'dev'
                }
            ]
        },
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'enesai'
                },
                {
                    'Key': 'env',
                    'Value': 'dev'
                }
            ]
        }
    ]
)
print("Instance Had been successfully created")