import boto3

def list_distributions(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('cloudfront')
    response = client.list_distributions(MaxItems='200')  
    if 'DistributionList' in response:
        if 'Items' in response['DistributionList']:
            return response['DistributionList']['Items'] #['ResponseMetadata']
    return []

def get_distribution(profile_name, distribution_id):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('cloudfront')
    response = client.get_distribution(Id=distribution_id)  
    return response['Distribution'] #['ResponseMetadata']

def invalid_distribuzion(profile_name, distribution_id):
    print("TODO" + profile_name +"|"+ distribution_id)
    return False

def main():
    print("Aws Py Console - CloudFront START")
    l=list_distributions("default")
    for e in l:
        print(e['Id'] + "|" + e['Status'] + "|" + e['Origins']['Items'][0]['DomainName'])
    if len(l)>0:
        d=get_distribution("default",l[0]['Id'])
        print(d)

if __name__ == '__main__':
    main()