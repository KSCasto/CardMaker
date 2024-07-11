'''
==========================================================
Any methods to create user-related data go in this section
'''
def addUserMethod(table,email):
    print(email)
    table.put_item(Item={'email':email})
    return 200

'''
==========================================================
Any methods to get user-related data go in this section
'''
def getUserMethod(table,email):
    res=table.get_item(Key={'email':email})
    if 'Item' in res:
        item=res['Item']
    else:
        item={"error":"email not found"}
    return item

def getAllUsersMethod(table):
    res=table.scan()
    items=res['Items']
    return items

'''
==========================================================
Any methods to update user-related data go in this section
'''
#I love you Kira - from Meep
def updateUserMethod(table,email,newAttributes):
    for attribute in newAttributes:
        # print(attribute)
        # res_obj = f"{attribute},{newAttributes[attribute]}"
        table.update_item(Key={'email':email},
        UpdateExpression='SET :att1 = :val1',
        ExpressionAttributeValues={
            ':att1': attribute,
            ':val1': newAttributes[attribute]
        })
    return 200

'''
==========================================================
Any methods to delete user-related data go in this section
'''
def deleteUserMethod(table,email):
    table.delete_item(Key={'email':email})
    return 200