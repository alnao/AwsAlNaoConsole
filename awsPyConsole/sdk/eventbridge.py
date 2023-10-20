import boto3

#see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html

def get_lista_regole(profile_name,prefix):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('events')
    if len(prefix)>0:
        response = client.list_rules(
            NamePrefix=prefix,
            EventBusName='default',
            #NextToken='string',
            Limit=100
        )
    else:
        response = client.list_rules(EventBusName='default',Limit=100)
    if "Rules" in response:
        return response['Rules']
    return []

def disable_role(profile_name,name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('events')
    response = client.disable_rule(
        Name=name,
        EventBusName='default'
    )
    return response
def enable_role(profile_name,name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('events')
    response = client.enable_rule(
        Name=name,
        EventBusName='default'
    )
    return response

def describe_rule(profile_name,name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('events')
    response = client.describe_rule(
        Name=name,
        EventBusName='default'
    )
    return response

def main():
    print("Aws Py Console - EventBridge START")
    lista= get_lista_regole("default","Alberto")
    for l in lista:
        print (l)
    print ("-------")
    o=describe_rule("default",lista[0]["Name"])
    print(o)

if __name__ == '__main__':
    main()