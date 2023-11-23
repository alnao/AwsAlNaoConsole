
import boto3
#import os
#import json
#import datetime
#import uuid
#from decimal import Decimal
#from boto3.dynamodb.conditions import Attr
#from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

def db_instances_list(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    rds_client = boto3.client('rds')
    response = rds_client.describe_db_instances(
                #DBInstanceIdentifier=instance_id
    )
    if "DBInstances" in response:
        return response["DBInstances"]
    return []

def main():
    print("Aws Py Console - RDS START")
    l=db_instances_list("default")
    print("-----------")
    for t in l:
        print(t)
    print("-----------")


if __name__ == '__main__':
    main()
