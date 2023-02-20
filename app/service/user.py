def addUserMethod(table,userInfo):
    table.put_item(Item=userInfo)
    return 200
#KIRAMAKES BIG POOPY

def getUserMethod(table,email):
    res=table.get_item(Key={'email':email})
    item=res['Item']
    return item
#THANKS FOR CODING BOTTOM

def getAllUsersMethod(table):
    res=table.scan()
    items=res['Items']
    return items

#I love you Kira - from Meep
def updateUserMethod(table,email,userInfo):
    return 200

def deleteUserMethod(table,email):
    table.delete_item(Key={'email':email})
    return 200