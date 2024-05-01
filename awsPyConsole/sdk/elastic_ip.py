import boto3
from botocore.exceptions import ClientError

#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-elastic-ip-addresses.html

def get_elastic_addresses(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    ec2 = boto3.client('ec2')
    filters = []#[{'Name': 'domain', 'Values': ['vpc']}]
    response = ec2.describe_addresses(Filters=filters)
    if 'Addresses' in response:
        return response['Addresses']
    return []

def allocate_address(profile_name,vpc,instance):
    boto3.setup_default_session(profile_name=profile_name)
    ec2 = boto3.client('ec2')
    try:
        allocation = ec2.allocate_address(Domain=vpc)
        response = ec2.associate_address(AllocationId=allocation['AllocationId'],InstanceId=instance)
        return response
    except ClientError as e:
        print(e)
        return e

def release_address(profile_name,allocationId):
    boto3.setup_default_session(profile_name=profile_name)
    ec2 = boto3.client('ec2')
    try:
        response = ec2.release_address(AllocationId='ALLOCATION_ID')
        return response
    except ClientError as e:
        print(e)
        return e

def main():
    print("Aws Py Console - Ec2 ElasticIP START")
    lista= get_elastic_addresses("default")
    print (lista)

if __name__ == '__main__':
    main()