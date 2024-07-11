import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

'''
==========================================================
Any methods to create user-related data go in this section
'''
def addUserMethod(table, email):
    try:
        logging.info(f"Adding user: {email}")
        table.put_item(Item={'email': email})
        return {"success": True, "status_code": 200}
    except Exception as e:
        logging.error(f"Error in addUserMethod: {str(e)}")
        return {"success": False, "error": str(e)}

'''
==========================================================
Any methods to get user-related data go in this section
'''
def getUserMethod(table, email):
    try:
        res = table.get_item(Key={'email': email})
        item = res.get('Item', {"error": "email not found"})
        return {"success": True, "data": item}
    except Exception as e:
        logging.error(f"Error in getUserMethod: {str(e)}")
        return {"success": False, "error": str(e)}

def getAllUsersMethod(table):
    try:
        res = table.scan()
        return {"success": True, "data": res['Items']}
    except Exception as e:
        logging.error(f"Error in getAllUsersMethod: {str(e)}")
        return {"success": False, "error": str(e)}

'''
==========================================================
Any methods to update user-related data go in this section
'''
#I love you Kira - from Meep
def updateUserMethod(table, email, newAttributes):
    try:
        for attribute, value in newAttributes.items():
            table.update_item(
                Key={'email': email},
                UpdateExpression='SET #attr = :val',
                ExpressionAttributeNames={'#attr': attribute},
                ExpressionAttributeValues={':val': value}
            )
        return {"success": True, "status_code": 200}
    except Exception as e:
        logging.error(f"Error in updateUserMethod: {str(e)}")
        return {"success": False, "error": str(e)}

'''
==========================================================
Any methods to delete user-related data go in this section
'''
def deleteUserMethod(table, email):
    try:
        table.delete_item(Key={'email': email})
        return {"success": True, "status_code": 200}
    except Exception as e:
        logging.error(f"Error in deleteUserMethod: {str(e)}")
        return {"success": False, "error": str(e)}