import boto3
from pprint import pprint

ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto')
volume= ec2_console.client(service_name='ec2', region_name='us-east-1')
#======================================================================

response = volume.describe_volumes()['Volumes']
# pprint(response)
for each_item in response:
    print("The volume id is: {}\nThe AvailabilityZone is: {}\nThe volume state is: {}".format(each_item['VolumeId'], each_item['AvailabilityZone'], each_item['State']))
    print("========================")