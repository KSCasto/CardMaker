import boto3

def connect():
    dynamodb = boto3.resource('dynamodb',region_name='us-west-1')
    return dynamodb
