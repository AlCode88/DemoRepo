import boto3
#===================== Lambda Settings ===============================
ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto')
ec2 = ec2_console.resource(service_name='ec2', region_name='us-east-1')

#===================== Create Snapshot with Looping =================================================
for instance in ec2.instances.filter(Filters=[{'Name': "instance-state-name",'Values': ["running"]}]):
    for device in instance.block_device_mappings:
        ec2.create_snapshot(VolumeId=device.get('Ebs').get('VolumeId'))
print("Snapshots has been created")