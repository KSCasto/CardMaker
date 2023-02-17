def addUserMethod(table,userInfo):
    table.put_item(Item=userInfo)
    return 200

def getUserMethod(table,email):
    res=table.get_item(Key={'email':email})
    item=res['Item']
    return item

def getAllUsersMethod(table):
    res=table.scan()
    items=res['Items']
    return items

def updateUserMethod(table,email,userInfo):
    return 200

def deleteUserMethod(table,email):
    table.delete_item(Key={'email':email})
    return 200