import json, logging
import boto3
from boto3.dynamodb.conditions import Key

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


'''
==========================================================
Any methods to create profiles go in this section
'''
def addProfile(table, user_id, profile_id, settings):
    try:
        item = {
            'user_id': user_id,
            'profile_id': profile_id,
            'settings': json.dumps(settings),
            **settings
        }
        response = table.put_item(Item=item)
        return response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        print(f"Error: {e}")
        return 500

'''
==========================================================
Any methods to get profiles go in this section
'''
def getProfile(table,user_id,profile_id):
    logging.info(f"user:{user_id}, profile:{profile_id}")
    res=table.get_item(Key={'user_id':user_id,'profile_id':profile_id})
    if 'Item' in res:
        item=res['Item']
    else:
        item={"error":"profile not found"}
    return item

def getAllUserProfiles(table,user_id):
    res=table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    items=res['Items']
    return items

def getAllProfiles(table):
    res=table.scan()
    items=res['Items']
    return items

'''
==========================================================
Any methods to update profiles go in this section
'''
def updateProfile(table, user_id, profile_id, newSettings):
    try:
        update_expr = "SET settings = :s, " + ", ".join(f"#{k} = :{k}" for k in newSettings)
        expr_values = {f":{k}": v for k, v in newSettings.items()}
        expr_values[":s"] = json.dumps(newSettings)
        expr_names = {f"#{k}": k for k in newSettings}

        logging.info(f"UpdateExpression: {update_expr}")
        logging.info(f"ExpressionAttributeValues: {expr_values}")
        logging.info(f"ExpressionAttributeNames: {expr_names}")
        
        response = table.update_item(
            Key={'user_id': user_id, 'profile_id': profile_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ExpressionAttributeNames=expr_names
        )
        return {"status_code": response['ResponseMetadata']['HTTPStatusCode']}
    except Exception as e:
        return {"error": str(e)}

'''
==========================================================
Any methods to delete profiles go in this section
'''
def deleteProfile(table,user_id,profile_id):
    table.delete_item(Key={'user_id':user_id,'profile_id':profile_id})
    return 200