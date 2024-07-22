# Automated EC2 Snapshot Cleanup

## Overview

This project automates the cleanup of unattached EC2 snapshots to optimize storage costs and maintain an efficient cloud environment. By identifying and deleting these orphaned snapshots, we can reduce unnecessary expenses and keep our AWS infrastructure clean.

## Project Components

- **AWS Lambda Function**: Automates the identification and deletion of unattached snapshots.
- **Boto3 Library**: Used for interacting with AWS EC2 services.
- **IAM Role**: Provides the Lambda function with the necessary permissions.

## Problem Statement

Snapshots are incremental backups created for data recovery. When EC2 instances or their volumes are deleted, their snapshots might remain, leading to avoidable storage costs over time.

## Solution

A Lambda function that:
1. Retrieves all snapshots, volumes, and instances.
2. Identifies snapshots not attached to any existing volumes.
3. Deletes the unattached snapshots to free up storage and reduce costs.

## Implementation Steps

1. **Set Up AWS Lambda Environment**
   - Created a Lambda function with IAM permissions for EC2 operations.

2. **Develop the Lambda Function**
   - **Code**: The Lambda function is developed in Python using the Boto3 library.(write cost-opt.py)
   - **Logic**:
     - Describe all snapshots, volumes, and instances.
     - Identify unattached snapshots.
     - Delete the unattached snapshots.

3. **Deploy and Test**
   - Deployed the Lambda function.
   - Tested to ensure proper operation and added logging for monitoring.

## Permissions Required

Create an IAM policy with the following JSON and attach it to the Lambda function's role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSnapshots",
                "ec2:DescribeVolumes",
                "ec2:DescribeInstances",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        }
    ]
}
