import boto3
#see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_trails.html
def list_trail(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('cloudtrail')
    response = client.list_trails(
       NextToken='string'
    )
    if 'Trails' in response:
        return  response['Trails']
    return []

def get_trail(profile_name, trail_name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('cloudtrail')
    response = client.get_trail(        Name=trail_name    )
    if 'Trail' in response:
        return response['Trail']
    return {}

def describe_trails(profile_name, trail_name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('cloudtrail')
    response = client.describe_trails(        trailNameList=[trail_name]    )
    if 'trailList' in response:
        return response['trailList']
    return []

def main():
    print("Aws Py Console - CloudFront START")
    l=list_trail("default")
    for e in l:
        print(e)
    if len(l)>0:
        print ("-------------")
        d=get_trail("default",l[0]['Name'])
        print (d)
        print ("-------------")
        dd=describe_trails("default",l[0]['Name'])
        print (dd)
        print ("-------------")


if __name__ == '__main__':
    main()
    