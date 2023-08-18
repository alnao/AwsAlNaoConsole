import boto3
#see https://docs.aws.amazon.com/code-library/latest/ug/python_3_ec2_code_examples.html
#see https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/ec2#code-examples

#see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-managing-instances.html


def get_lista_istanze(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    return response

def main():
    print("Aws Py Console - Ec2 Instances START")
    lista= get_lista_istanze("default")
    print (lista)

if __name__ == '__main__':
    main()