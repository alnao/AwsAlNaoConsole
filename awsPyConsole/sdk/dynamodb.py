import boto3
import os
import json
import datetime
import uuid
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

def table_list(profile_name):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('dynamodb')
    response = client.list_tables(    Limit=100)
    tables = []
    for table in response['TableNames']:
        tables.append(table)
    return tables

def write_element_with_id(profile_name, table,element):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('dynamodb')
    if 'id' not in element:
        element['id'] = str(uuid.uuid4()) #calcolo id univoco
    ts= TypeSerializer()
    serialized_post= ts.serialize(element)["M"]
    res = client.put_item(TableName=table,Item=serialized_post)
    res['id']=element['id']
    return res

def get_element_by_id(profile_name,table,id):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('dynamodb')
    response = client.get_item(    Key={ 'id': {'S': id,        } } ,    TableName=table,)
    return response['Item']
    
def delete_element_by_id(profile_name,table,id):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('dynamodb')
    response = client.delete_item(    Key={ 'id': {'S': id,        } } ,    TableName=table,)
    return response

def scan_table(profile_name,table):
    boto3.setup_default_session(profile_name=profile_name)
    client = boto3.client('dynamodb')
    response = client.scan(
    #    ExpressionAttributeNames={
    #        '#AT': 'AlbumTitle',
    #        '#ST': 'SongTitle',
    #    },
    #    ExpressionAttributeValues={
    #        ':a': {
    #            'S': 'No One You Know',
    #        },
    #    },
    #    FilterExpression='Artist = :a',
    #    ProjectionExpression='#ST, #AT',
        TableName=table,
    #    Limit=123,
    )
    return response['Items']
def full_scan_table(profile_name,table):
    boto3.setup_default_session(profile_name=profile_name)
    dynamodb = boto3.resource('dynamodb')#, region_name="eu-west-1"
    table = dynamodb.Table(table)
    today = datetime.datetime.now()
    response = table.scan( ) #FilterExpression=Attr('country').eq('US') & Attr('city').eq('NYC')
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'],  ) #FilterExpression
        data.extend(response['Items'])
    return data 

# aggiunto in sviluppo 12 maggio 23 per test rotto, non produzione. 
# https://stackoverflow.com/questions/69104540/python-json-typeerror-object-of-type-decimal-is-not-json-serializable
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def main():
    print("Aws Py Console - DynamoDB START")
    l=table_list("default")
    print("-----------")
    for t in l:
        print(t)
    print("-----------")
def a():
    r=write_element_with_id("default","dynamo-es12",{'Name' : 'Alberto'})
    id=r['id']
    print(r)
    print("-----------")
    e=get_element_by_id("default","dynamo-es12",id)
    print(e)
    print("-----------")
    t=scan_table("default","dynamo-es12")
    for et in t:
        print(et)
    print("-----------")
    t=full_scan_table("default","dynamo-es12")
    for et in t:
        print(et)
    print("-----------")
    d=delete_element_by_id("default","dynamo-es12",id)
    print(d)
    print("----------- END")

if __name__ == '__main__':
    main()
