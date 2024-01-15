import json
import boto3
#see https://unbiased-coder.com/python-aws-boto3-sns-guide/

def get_sns_list(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    sns_client = boto3.client('sns')
    topics_iter = sns_client.list_topics()
    if 'Topics' in topics_iter :
        return topics_iter['Topics']
    return []

def create_topic(profile_name, topic_name):
    boto3.setup_default_session(profile_name=profile_name)
    sns_client = boto3.client('sns')
    topic = sns_client.create_topic(Name=topic_name)
    return topic

def delete_topic(profile_name, topic_arn):
    boto3.setup_default_session(profile_name=profile_name)
    sns_client = boto3.client('sns')
    topic = sns_client.delete_topic(TopicArn=topic_arn)
    return topic

def subscribe_topic(profile_name, topic_arn,email):
    boto3.setup_default_session(profile_name=profile_name)
    sns = boto3.client('sns')
    sns_resource = boto3.resource('sns')
    topics_iter = sns.list_topics()
    if 'Topics' in topics_iter :
        for element in topics_iter['Topics']:
            if topic_arn==element['TopicArn']:
                topic_arn = element['TopicArn']
                topic = sns_resource.Topic(arn=topic_arn)
                subscription = topic.subscribe(Protocol='email', Endpoint=email, ReturnSubscriptionArn=True)
                return subscription
    return {}

def get_subscriptions(profile_name,topic_arn):
    boto3.setup_default_session(profile_name=profile_name)
    sns_client = boto3.client('sns')
    subscriptions = sns_client.list_subscriptions()
    if 'Subscriptions' in subscriptions:
        list=[]
        for el in subscriptions['Subscriptions']:
            if topic_arn == el['TopicArn']:
                list.append(el)
        return list
    return []

def publish(profile_name,topic_arn,post):
    boto3.setup_default_session(profile_name=profile_name)
    #sns_client = boto3.client('sns')
    sns_resource = boto3.resource('sns')
    topic = sns_resource.Topic(arn=topic_arn)
    result = topic.publish(Message=post)
    return result

def main():
    print("Aws Py Console - Ec2 Instances START")
    #create
    #result= create_topic("default","AlbertoSDK")
    #print(result)
    #print ("----------------------------------------------------------------")
    
    #list
    lista= get_sns_list("default")
    print (lista)
    print ("----------------------------------------------------------------")
    arn= "arn:aws:sns:eu-west-1:xxxxxxxx:AlbertoSDK" # result['TopicArn']
    
    #subscrive
    #res = subscribe_topic("default", arn, "alberto.nao@cherrybank.it")
    #print (res)
    #print ("----------------------------------------------------------------")

    #list subscription
    res=get_subscriptions("default",arn)
    print( res )
    print ("----------------------------------------------------------------")

    #publish content in topic
    res=publish("default",arn,"topic post message")
    print( res )
    print ("----------------------------------------------------------------")

    #delete topic
    #result= delete_topic("default",arn )
    #print(result)    

if __name__ == '__main__':
    main()