import boto3
#see https://docs.aws.amazon.com/code-library/latest/ug/python_3_ec2_code_examples.html
#see https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/ec2#code-examples

#see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-managing-instances.html
#see #https://medium.com/featurepreneur/using-ec2-services-using-boto3-ad5453fe3bea

def get_lista_istanze(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    return response

def set_tag(instance_id, tag_key, tag_value):
    if tag_key=='':
        return
    ec2 = boto3.resource('ec2')# region_name=AWS_REGION)
    tags=[{'Key': tag_key,'Value': tag_value}]
    instances = ec2.instances.filter(InstanceIds=[instance_id,],)
    for instance in instances:
        instance.create_tags(Tags=tags)
    print("set_tag "  + instance_id)
    return tags

#https://medium.com/featurepreneur/using-ec2-services-using-boto3-ad5453fe3bea
def stop_instance(instance_id):
    ec2_client = boto3.client('ec2')#, region_name=”us-west-2"
    print ("stop_instance " + instance_id)
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    return response

def start_instance(instance_id):
    ec2_client = boto3.client('ec2')
    print ("start_instance " + instance_id)
    response = ec2_client.start_instances(InstanceIds=[instance_id])
    return response

#def terminate_instance(instance_id):

def main():
    print("Aws Py Console - Ec2 Instances START")
    lista= get_lista_istanze("default")
    print (lista)

if __name__ == '__main__':
    main()