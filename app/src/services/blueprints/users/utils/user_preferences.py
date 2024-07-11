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
        return {"success": True, "status_code": response['ResponseMetadata']['HTTPStatusCode']}
    except Exception as e:
        logging.error(f"Error in addProfile: {str(e)}")
        return {"success": False, "error": str(e)}

'''
==========================================================
Any methods to get profiles go in this section
'''
def getProfile(table,user_id,profile_id):
    try:
        logging.info(f"user:{user_id}, profile:{profile_id}")
        res=table.get_item(Key={'user_id':user_id,'profile_id':profile_id})
        item = res.get('Item', {"error": "profile not found"})
        return {"success": True, "data": item}
    except Exception as e:
        logging.error(f"Error in getProfile: {str(e)}")
        return {"success": False, "error": str(e)}

def getAllUserProfiles(table,user_id):
    try:
        res = table.query(KeyConditionExpression=Key('user_id').eq(user_id))
        return {"success": True, "data": res['Items']}
    except Exception as e:
        logging.error(f"Error in getAllUserProfiles: {str(e)}")
        return {"success": False, "error": str(e)}

def getAllProfiles(table):
    try:
        res = table.scan()
        return {"success": True, "data": res['Items']}
    except Exception as e:
        logging.error(f"Error in getAllProfiles: {str(e)}")
        return {"success": False, "error": str(e)}

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
        return {"success": True, "status_code": response['ResponseMetadata']['HTTPStatusCode']}
    except Exception as e:
        logging.error(f"Error in updateProfile: {str(e)}")
        return {"success": False, "error": str(e)}

'''
==========================================================
Any methods to delete profiles go in this section
'''
def deleteProfile(table,user_id,profile_id):
    try:
        table.delete_item(Key={'user_id': user_id, 'profile_id': profile_id})
        return {"success": True, "status_code": 200}
    except Exception as e:
        logging.error(f"Error in deleteProfile: {str(e)}")
        return {"success": False, "error": str(e)}