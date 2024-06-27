import boto3
import pyotp, os, base64
from .db import connect

def authenticate(uid,token):
    dynamodb = connect()
    table=dynamodb.Table('user_auth')
    res=table.get_item(Key={
        'user_id':uid,
        'token':token
    })
    return ('Item' in res)
