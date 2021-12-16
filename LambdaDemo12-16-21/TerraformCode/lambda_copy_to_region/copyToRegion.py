import boto3
import json

def lambda_handler(event, context):
    ############ Variables and Client ##########################################
    source_region = 'us-east-1'
    destination_region = 'us-east-2'
    ec2_source_client=boto3.client(service_name='ec2', region_name=source_region)
    
    ################ Get your Account ID ########################################
    sts_client = boto3.client(service_name='sts', region_name=source_region)
    account_ids= sts_client.get_caller_identity()['Account']
    
    
    ############# Collect all Snapshots that you would like to copy #####################################################
    source_snapshot_filter = {'Name':'tag:Name', 'Values':['enesai']}
    backup_snapshots = []
    for each_snap in ec2_source_client.describe_snapshots(OwnerIds=[account_ids],Filters=[source_snapshot_filter])['Snapshots']:
        print(each_snap['SnapshotId'])
        backup_snapshots.append(each_snap['SnapshotId'])
    print("All available snapshots under filter", backup_snapshots)
    
    
    ############## Destination Variables and Client #########################################
    ec2_destination_client = boto3.client(service_name='ec2', region_name=destination_region)
    
    for each_source_snapid in backup_snapshots:
        print ("Taking backup of {} inot a {}".format(each_source_snapid,destination_region))
        ec2_destination_client.copy_snapshot(
            Description="This is encrypted copy of us-east-1 snap",
            Encrypted=True,
            SourceRegion=source_region,
            SourceSnapshotId=each_source_snapid,
            TagSpecifications=[
              {
                'ResourceType': 'snapshot',
                'Tags': [
                    {
                    'Key': 'Name',
                    'Value': 'enesai'
                    },
                    {
                    'Key': 'CopyRegion',
                    'Value': 'us-east-1'
                    },
                    {
                    'Key': 'Source_snap',
                    'Value': 'enesai_us-east-1'
                    }
                ]
              }
            ]
        )
    print("Copying Snapshot is completed")
    
    ############## Modifiying snapshots for completed Tags #####################################
    print("Modifiyig Tags for the snapshots that has been completed the backup")
    for each_source_snapid in backup_snapshots:
        print("Deleting old tags {}".format(each_source_snapid))
        ec2_source_client.delete_tags(
            Resources=[each_source_snapid],
            Tags = [
                {
                    'Key':'Name',
                    'Value':'enesai'
                }
            ]
        )
        print("Creating New Tags {}".format(each_source_snapid))
        ec2_source_client.create_tags(
            Resources=[each_source_snapid],
            Tags = [
                {
                    'Key':'Name',
                    'Value':'enesai_snap_completed'
                }
            ]
        )