import boto3
from datetime import datetime

########### Filters Variables and Clients ##############################
ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto') 
ec2_re= ec2_console.resource(service_name="ec2",region_name="us-east-1")                                                       

#============== Filters ====================================
enesai_volume_ids = {'Name':'tag:Name', 'Values':['enesai']}                                                                                                                
enesai_snaps = {'Name':'tag:env', 'Values':['dev']}

#============== Lists for snaps and volumes =================
snapshot_ids=[]
snap_ids=[]
vol_ids=[]

########### Colleting volume Ids ###################################           
for each_vol in ec2_re.volumes.filter(Filters=[enesai_volume_ids]):                                                                                                                                                                         
    vol_ids.append(each_vol.id)                                                                                                                                                                                                              
print('All volume ids are: ',vol_ids)              
                                                                                                                          
########## Creating snapshots for tagged volumes ######################
print('Creating a Snapshots for dev volumes') 
for each_volume_id in vol_ids:                                                                                                
    response= ec2_re.create_snapshot(                                                                                      
    Description='Snap with Lambda',                                                                                       
    VolumeId=each_volume_id,                                                                                                  
    TagSpecifications=[                                                                                                   
        {                                                                                                              
            'ResourceType': 'snapshot',                                                                                   
             'Tags': [                                                                                                    
                {                                                                                                         
                    'Key': 'Delete-on',                                                                                   
                    'Value':'90'                                                                                          
                },
                {                                                                                                         
                    'Key': 'Name',                                                                                   
                    'Value':'enesai'                                                                                          
                },
                {                                                                                                         
                    'Key': 'env',                                                                                   
                    'Value':'dev'                                                                                          
                }                                                                                                        
            ]                                                                                                   
        }                                                                                                               
    ]                                                                                                                  
)                                                                                                                    
snap_ids.append(response.id)                                                                                           
                                                                                             
########### Creating waiter using client  ########################
ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto') 
ec2_cli=ec2_console.client(service_name="ec2",region_name="us-east-1")                                                        
waiter = ec2_cli.get_waiter('snapshot_completed')                                                                         
waiter.wait(SnapshotIds=snap_ids)

########## Define UTC time zone ##########
now = datetime.now()
time = now.strftime("%m-%d-%Y  %H-%M-%S")

############## Variables and boto client ###########################################################
ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto')
list_ec2_snaps = ec2_console.client(service_name='ec2', region_name='us-east-1')

################## List all snapshots   ###################################################################
print('Listing All Snapshots')
for each_snap in list_ec2_snaps.describe_snapshots(Filters=[enesai_snaps],OwnerIds=['self'])['Snapshots']:
    snapshot_ids.append(each_snap['SnapshotId'])
print(snapshot_ids)

################# create a AMI from snapshops with Functions ######################
def creat_images_from_snap():
    for snapshots in snapshot_ids:
        print("Creating Imagesf for dev snapsshot {}".format(snapshots))
        name = "enesai-image"
        image = list_ec2_snaps.register_image(
            BlockDeviceMappings=[
                 {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'SnapshotId':snapshots,
                        'VolumeSize': 8,
                        'VolumeType': 'gp2'
                    }
                 },
            ],
            Description='create enesa AMIs',
            Name=name,
            RootDeviceName='/dev/sda1',
            VirtualizationType='hvm'
        )
    print("Images for dev snapshot has been created")
creat_images_from_snap()

########### Creating waiter using client  ########################
# ec2_console = boto3.session.Session(profile_name='DemoLambdaBoto') 
# ec2_cli=ec2_console.client(service_name="ec2",region_name="us-east-1")                                                        
# waiter = ec2_cli.get_waiter('image_available')                                                                         
# waiter.wait(ImageIds=)