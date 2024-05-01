import json
import boto3
from datetime import datetime 
#see https://hands-on.cloud/boto3-sqs-tutorial/

#see https://github.com/boto/botocore/issues/2705
import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='botocore.client')


def get_sns_list(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    sqs_client = boto3.client("sqs") #, region_name=AWS_REGION
    topics_iter = sqs_client.list_queues(
        #QueueNamePrefix='string',
        #NextToken='string',
        MaxResults=100
    )
    if 'QueueUrls' in topics_iter :
        return topics_iter['QueueUrls']
    return []

def create_queue(profile_name, queue_name,delay_seconds,visiblity_timeout):
    boto3.setup_default_session(profile_name=profile_name)
    sqs_client = boto3.client("sqs") #, region_name=AWS_REGION
    response = sqs_client.create_queue(QueueName=queue_name,
        Attributes={
            'DelaySeconds': str(delay_seconds),
            'VisibilityTimeout': str(visiblity_timeout)
            #  'FifoQueue': 'true'
        })
    return response

def delete_queue(profile_name, queue_name):
    boto3.setup_default_session(profile_name=profile_name)
    sqs_client = boto3.client("sqs") #, region_name=AWS_REGION
    response = sqs_client.delete_queue(QueueUrl=queue_name)
    return response

def get_queue(profile_name, queue_url):
    boto3.setup_default_session(profile_name=profile_name)
    sqs_client = boto3.client("sqs") #, region_name=AWS_REGION
    #response = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
    response = sqs_client.get_queue_attributes(    QueueUrl=queue_url, AttributeNames=['All'])
    if 'Attributes' in response:
        return response['Attributes']
    return {}
    
def send_queue_message(profile_name,queue_url,msg_attributes,msg_body):
    boto3.setup_default_session(profile_name=profile_name)
    sqs_client = boto3.client("sqs") #, region_name=AWS_REGION
    response = sqs_client.send_message(QueueUrl=queue_url,
        MessageAttributes=msg_attributes,
        MessageBody=msg_body)
    return response

def receive_queue_messages(profile_name,queue_url):
    boto3.setup_default_session(profile_name=profile_name)
    sqs_client = boto3.client("sqs") #, region_name=AWS_REGION
    response = sqs_client.receive_message(QueueUrl=queue_url,MaxNumberOfMessages=10)
    if 'Messages' in response:
        return response['Messages']
    return []

def delete_queue_message(profile_name,queue_url, receipt_handle):
    boto3.setup_default_session(profile_name=profile_name)
    sqs_client = boto3.client("sqs") #, region_name=AWS_REGION
    response = sqs_client.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)
    return response

def main(profile):
    print("Aws Py Console - SQS Instances START")
    #create
    #result= create_queue(profile,"formazione-sqs-sdk",10,10)
    #print(result)
    print ("----------------------------------------------------------------")
    
    #list
    lista= get_sns_list(profile)
    print (lista)
    print ("----------------------------------------------------------------")
    QUEUE_URL=lista[1] 

    #get_queue
    res = get_queue(profile, QUEUE_URL)
    json_msg = json.dumps(res, indent=4)
    print (json_msg)
    print ("----------------------------------------------------------------")
    
    #send_message
    MSG_ATTRIBUTES = {'Author': {'DataType': 'String','StringValue': 'Alberto Nao' }    }
    MSG_BODY = "Message from SDK to SQS "+datetime.today().strftime('%Y%m%d %H%M%S')
    res=send_queue_message(profile,QUEUE_URL,MSG_ATTRIBUTES,MSG_BODY)
    #json_msg = json.dumps(res, indent=4)
    print( res )
    print ("----------------------------------------------------------------")

    #read messages
    messages = receive_queue_messages(profile,QUEUE_URL)
    #print (messages)
    for msg in messages:
        #print (msg) MessageId,ReceiptHandle,Body, MD5OfBody
        msg_body = msg['Body']
        receipt_handle = msg['ReceiptHandle']
        print(f'The message body: {msg_body}')
        delete_queue_message(profile,QUEUE_URL, receipt_handle)
    

    #delete topic
    #result= delete_queue("default","formazione-sqs-sdk" )
    #print(result)    

if __name__ == '__main__':
    main("default")