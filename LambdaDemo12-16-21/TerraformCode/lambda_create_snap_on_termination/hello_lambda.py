import boto3
import json

def lambda_handler(event, context):
    volume = boto3.client(service_name='ec2', region_name='us-east-1')
    list_of_volumes=[]
    enesai_volume_ids = {'Name':'tag:Name', 'Values':['enesai']}
    
    for each_volume in volume.describe_volumes(Filters=[enesai_volume_ids])['Volumes']:
        list_of_volumes.append(each_volume['VolumeId'])
    print("The enesai volume ids are:  ",list_of_volumes)
    
    
    #4 Create a Snapshot with Client
    snapshot_ids=[]
    for each_snapshot in list_of_volumes:
        print("Taking the snap of {}".format(each_snapshot))
        response=volume.create_snapshot(
            Description='Create a snapshot for Lambda Functions',
            VolumeId=each_snapshot,
            TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'enesai'
                    }
                ]
            }
        ]
        )
        snapshot_ids.append(response['SnapshotId'])
    print ("The snap ids are: ",snapshot_ids)

    waiter = volume.get_waiter('snapshot_completed')
    waiter.wait(SnapshotIds=snapshot_ids)

    print ("Successfully completed snaps for the volumes of: {}".format(list_of_volumes))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello form Lambda!')
    }