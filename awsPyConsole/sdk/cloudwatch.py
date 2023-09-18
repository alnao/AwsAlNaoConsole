import boto3
from datetime import datetime, timedelta
import time

#see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html#
#see log https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html
#see alarm https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-examples.html


def get_metrics(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    cloudwatch = boto3.client('cloudwatch')
    lista=[]
    paginator = cloudwatch.get_paginator('list_metrics')
    for response in paginator.paginate(Dimensions=[{'Name': 'LogGroupName'}],
                                    MetricName='IncomingLogEvents',
                                    Namespace='AWS/Logs'):
        lista=lista+response['Metrics']
    return lista

#{'Namespace': 'AWS/Logs', 'MetricName': 'IncomingLogEvents', 'Dimensions': 
# [{'Name': 'LogGroupName', 'Value': '/aws/lambda/provaBoto3risorse'}]}
def put_metrics(profile_name, metric_name,metric_dim_name,metric_dim_val,matric_unit,metric_value,name_space):
    # Put custom metrics
    boto3.setup_default_session(profile_name=profile_name)
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(
        MetricData=[ 
             {
                'MetricName': metric_name,#'PAGES_VISITED',
                'Dimensions': [
                    {
                        'Name':metric_dim_name,# 'UNIQUE_PAGES',
                        'Value':metric_dim_val#, 'URLS'
                    },
                ],
                'Unit': matric_unit,#'None',
                'Value': metric_value# 1.0
            },
        ],
        Namespace=name_space #'SITE/TRAFFIC'
    )

def get_metric_group_log(profile_name,group_name):
    # Create CloudWatchLogs client
    boto3.setup_default_session(profile_name=profile_name)
    cloudwatch_logs = boto3.client('logs')
    # List subscription filters through the pagination interface
    paginator = cloudwatch_logs.get_paginator('describe_log_groups')
    lista=[]
    for response in paginator.paginate(logGroupNamePrefix=group_name):
        lista=lista+response['logGroups']
        #for i in response['logGroups']:
            #print(i['logGroupName'])
    return lista

def get_metric_log(profile_name,group_name,hours):
    boto3.setup_default_session(profile_name=profile_name)
    cloudwatch_logs = boto3.client('logs')
    query = "fields @timestamp, @message"
    start_query_response = cloudwatch_logs.start_query(
        logGroupName=group_name,
        startTime=int((datetime.today() - timedelta(hours=hours)).timestamp()),
        endTime=int(datetime.now().timestamp()),
        queryString=query,
    )
    query_id = start_query_response['queryId']
    response = None
    while response == None or response['status'] == 'Running':
        #print('Waiting for query to complete ...')
        time.sleep(1)
        response = cloudwatch_logs.get_query_results(
            queryId=query_id
        )
    return response["results"]

def main():
    print("Aws Py Console - Ec2 Instances START")
    lista= get_metrics("default")
    if len(lista)>0:
        print (lista[0])
    lamnda="K4FDocFromItalsoft-K4FDoc-DocFromItalsoftSftpLambd-DkOR4fJXTlB6"
    lista= get_metric_group_log("default","/aws/lambda/"+lamnda )
    if len(lista)>0:
        print (lista[0])
    lista=get_metric_log("default","/aws/lambda/"+lamnda ,10)
    if len(lista)>0:
        print (lista[0])
    else:
        print("Nessun log")

if __name__ == '__main__':
    main()