import boto3

def api_list(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('apigateway')
    response = client.get_rest_apis(       limit=100    )
    if 'items' in response:
        return response['items']
    return []

def resouce_list(profile_name,api_ip):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('apigateway')
    response = client.get_resources(        restApiId=api_ip,        limit=100)
    if 'items' in response:
        return response['items']
    return []

def method_detail(profile_name,api_ip,resouce_id,method):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('apigateway')
    response = client.get_method(restApiId=api_ip,resourceId=resouce_id,httpMethod=method)
    return response

def stage_list(profile_name,api_ip):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('apigateway')
    response = client.get_stages(        restApiId=api_ip)
    if 'item' in response:
        return response['item']
    return response

def main():
    print("Aws Py Console - ApiGateway START")
    l=api_list("default")
    for e in l:
        print(e['id'] + "|" + e['name'] + "|" + str(e['createdDate']) )
    if len(l)>0:
        print("--------")
        d=resouce_list("default",l[0]['id'])
        for e in d:
            print(e)
        if len(d)>0:
            print("--------")
            if 'GET' in d[0]['resourceMethods']:
                m=method_detail("default",l[0]['id'],d[0]['id'],'GET' )
                print(m)
        print("--------")
        s=stage_list("default",l[0]['id'])
        for e in s:
            print(e)
        print("--------")

if __name__ == '__main__':
    main()