import boto3

ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto')
volume = ec2_console.client(service_name='ec2', region_name='us-east-1')

# ============ Filtering ==================================
list_of_volumes=[]
enesai_volume_ids = {'Name':'tag:Name', 'Values':['enesai']}

#============== List enesai volumes ==============================================   
for each_volume in volume.describe_volumes(Filters=[enesai_volume_ids])['Volumes']:
    list_of_volumes.append(each_volume['VolumeId'])
print("The enesai volume ids are:  ",list_of_volumes)