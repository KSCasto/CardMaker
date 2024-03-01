import boto3
import pyotp, os, base64
from db import connect

def authenticate(email,pw):
    dynamodb = connect()
    table=dynamodb.Table('user_auth')
    res=table.get_item(Key={
        'email':email,
        'pw':pw
    })
    return ('Item' in res)
