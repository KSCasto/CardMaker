import sys
#This import is from the perspective of app.py in the app parent directory
from services.blueprints.users.utils import user

from flask import Flask,Blueprint,request
from services.utils import db

app = Blueprint('users',__name__)

@app.route("/user",methods = ['POST','PUT','GET','DELETE'])
def addUser():
    dynamodb=db.connect()
    table=dynamodb.Table('users')
    res_obj={}
    if request.method == 'POST':
        user_data=request.json
        if ("email" in user_data):
            email=user_data["email"]
            print(email)
            user.addUserMethod(table, email)
            res_obj=user.getUserMethod(table,email)
        else:
            res_obj="Missing key 'email' in body"
    elif request.method == 'PUT':
        res_obj=user.updateUserMethod(table, request.args.get("user"),request.json)
        # res_obj=user.getUserMethod(table,request.args.get("user"))
    elif request.method == 'GET':
        if request.args.get("user"):
            res_obj=user.getUserMethod(table, request.args.get("user"))
        else:
            res_obj=user.getAllUsersMethod(table)
    elif request.method == 'DELETE':
        user.deleteUserMethod(table,request.args.get("user"))
        res_obj=f"User {request.args.get('user')} deleted"
    return res_obj