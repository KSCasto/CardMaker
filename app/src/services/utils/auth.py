import boto3
import pyotp, os, string, logging
import base64, secrets
import traceback
from .db import connect

# Make a password with 32 bits of entropy using letters and digits
def generate_user_token():
    charset = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(charset) for _ in range(32))
    return token

def authenticate(uid,token):
    dynamodb = connect()
    table = dynamodb.Table('user_auth')
    res = table.get_item(Key={
        'user_id':uid
    })

    user_authorized=False
    if 'Item' not in res:
        newToken = generate_user_token()
        authItem = {
            'user_id': uid,
            'token': newToken
        }
        #table should still be user_auth at this point
        try:
            table.put_item(
                Item=authItem
            )
        except Exception as e:
            logging.info(f"Exception Occurred: {type(e).__name__}")
            logging.info(f"Msg: {str(e)}")
            logging.info("Traceback:")
            logging.info(traceback.format_exc())
        # userItem={}
    elif 'Item' in res: 
        if 'token' in res['Item'] and token == res['Item']['token']:
            user_authorized = True

    return user_authorized
