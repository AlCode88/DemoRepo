import boto3
from pprint import pprint
#================= Settings ========================================
ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto')
ec2 = ec2_console.client(service_name='ec2', region_name='us-east-1')

#=================== Describe Instance Loop ========================
response = ec2.describe_instances()['Reservations']
print (response)

for each_item in response:
   for each_info in each_item['Instances']:
       print("The image id is: {}\nThe instance id is: {}\nThe Instance Launch Time is: {}".format(each_info['ImageId'], each_info['InstanceId'], each_info['LaunchTime'].strftime("%Y-%m-%d")))
       print("=======================================")