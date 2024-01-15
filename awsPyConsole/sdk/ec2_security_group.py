import boto3
#see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/index.html

def get_list(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_security_groups()
    if 'SecurityGroups' in response:
        return response['SecurityGroups']
    return []

def main():
    print("Aws Py Console - Ec2 Instances START")
    lista= get_list("default")
    print (lista)

if __name__ == '__main__':
    main()

#https://docs.aws.amazon.com/it_it/AWSEC2/latest/UserGuide/example_ec2_CreateSecurityGroup_section.html
class SecurityGroupWrapper:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) security group actions."""

    def __init__(self, ec2_resource, security_group=None):
        """
        :param ec2_resource: A Boto3 Amazon EC2 resource. This high-level resource
                             is used to create additional high-level objects
                             that wrap low-level Amazon EC2 service actions.
        :param security_group: A Boto3 SecurityGroup object. This is a high-level object
                               that wraps security group actions.
        """
        self.ec2_resource = ec2_resource
        self.security_group = security_group

    @classmethod
    def from_resource(cls):
        ec2_resource = boto3.resource("ec2")
        return cls(ec2_resource)


    def create(self, group_name, group_description):
        """
        Creates a security group in the default virtual private cloud (VPC) of the
        current account.

        :param group_name: The name of the security group to create.
        :param group_description: The description of the security group to create.
        :return: A Boto3 SecurityGroup object that represents the newly created security group.
        """
        try:
            self.security_group = self.ec2_resource.create_security_group(
                GroupName=group_name, Description=group_description
            )
        except Exception as err:
            print(
                "Couldn't create security group %s. Here's why: %s: %s",
                group_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return self.security_group