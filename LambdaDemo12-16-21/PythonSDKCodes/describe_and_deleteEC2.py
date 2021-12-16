import boto3

#=================== Settings ==========================================
ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto')
ec2_resource = ec2_console.resource('ec2', region_name='us-east-1')

#=================== Describe EC2 Instance =============================
enesai_tag_instance=[]
filters = {"Name": 'tag:Name', "Values":['enesai']}

for each_ec2 in ec2_resource.instances.filter(Filters=[filters]):
    enesai_tag_instance.append(each_ec2.id)
print(enesai_tag_instance)


#========================== Terminate Enesai Instance ===================
print("Terminating Enesai Instance ......")
ec2_resource.instances.filter(InstanceIds=enesai_tag_instance).terminate()
print("Enesai Instance Got Terminated")