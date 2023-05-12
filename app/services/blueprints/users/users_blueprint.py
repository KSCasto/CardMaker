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
        user.addUserMethod(table, request.json)
    elif request.method == 'PUT':
        res_obj=request.json
        user.updateUserMethod(table, request.args.get("user"),request.body)
    elif request.method == 'GET':
        if request.args.get("user"):
            res_obj=user.getUserMethod(table, request.args.get("user"))
        else:
            res_obj=user.getAllUsersMethod(table)
    elif request.method == 'DELETE':
        user.deleteUserMethod()
    return res_obj