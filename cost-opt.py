import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get a list of all snapshots
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    print(f"Total Snapshots: {len(snapshots)}")
    
    # Get a list of all volumes
    volumes = ec2.describe_volumes()['Volumes']
    print(f"Total Volumes: {len(volumes)}")
    
    # Create a set of volume IDs
    volume_ids = {volume['VolumeId'] for volume in volumes}
    print(f"Volume IDs: {volume_ids}")
    
    # Get a list of all instances
    instances = ec2.describe_instances()['Reservations']
    instance_ids = {instance['InstanceId'] for reservation in instances for instance in reservation['Instances']}
    print(f"Instance IDs: {instance_ids}")
    
    # Find unattached snapshots
    unattached_snapshots = [snapshot for snapshot in snapshots if snapshot['VolumeId'] not in volume_ids]
    print(f"Unattached Snapshots: {unattached_snapshots}")
    
    deleted_snapshots = []
    
    # Delete unattached snapshots
    for snapshot in unattached_snapshots:
        snapshot_id = snapshot['SnapshotId']
        try:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            deleted_snapshots.append({
                'SnapshotId': snapshot_id,
                'VolumeId': snapshot['VolumeId'],
                'Description': snapshot['Description']
            })
            print(f"Deleted Snapshot ID: {snapshot_id}, Volume ID: {snapshot['VolumeId']}, Description: {snapshot['Description']}")
        except Exception as e:
            print(f"Failed to delete Snapshot ID: {snapshot_id}, error: {str(e)}")
    
    # Return deleted snapshots in the response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'deleted_snapshots': deleted_snapshots
        })
    }
