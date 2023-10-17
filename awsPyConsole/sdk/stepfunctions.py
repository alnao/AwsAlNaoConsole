import boto3


def state_machine_list(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('stepfunctions')
    response = client.list_state_machines(maxResults=100)
    if 'stateMachines' in response:
        return response['stateMachines']
    return[]

def state_machine_detail(profile_name,smArn):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('stepfunctions')
    response = client.describe_state_machine(    stateMachineArn=smArn)
    return response

def state_machine_execution(profile_name,smArn):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('stepfunctions')
    response = client.list_executions(
        stateMachineArn=smArn,
        #statusFilter='RUNNING'|'SUCCEEDED'|'FAILED'|'TIMED_OUT'|'ABORTED',
        maxResults=100,
        #nextToken='string',
        #mapRunArn='string'
    )
    if 'executions' in response:
        return response['executions']
    return []

def state_machine_execution_detail(profile_name,esecutionArn):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('stepfunctions')
    response = client.describe_execution(executionArn=esecutionArn)
    return response
    #see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/client/describe_execution.html

def state_machine_start(profile_name,stateMachineArn,name,input):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('stepfunctions')
    response = client.start_execution(        stateMachineArn=stateMachineArn,       name=name,        input=input   )
    return response
    #see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/client/start_execution.html

def main():
    print("Aws Py Console - Step functions START")
    print("-----------")
    lista_b= state_machine_list("default")
    for b in lista_b:
        print (b["name"] + "|" + b["type"] + "|" + b["stateMachineArn"] + "|" + str(b["creationDate"]) )
    print("-----------")
    if len(lista_b)==0:
        return
    r=state_machine_detail("default",lista_b[12]['stateMachineArn'])
    print ( r )
    print("-----------")
    r=state_machine_execution("default",lista_b[12]['stateMachineArn'])
    print ( r )
    print("-----------")
    if len(r)>0:
        r=state_machine_execution_detail("default",r[0]['executionArn'])
        print ( r )
        print("-----------")
#    r=state_machine_start("default",lista_b[12]['stateMachineArn'],"testByBoto3", "{ \"filename\": \"prova.csv\" , \"SkipDeleteSourceFile\" : false }" )
#    print ( r )
#    print("-----------")
    r=state_machine_execution("default",lista_b[12]['stateMachineArn'])
    print ( r )
    print("----------- END")

if __name__ == '__main__':
    main()
