import boto3
import requests, json, os, sys
from flask import Flask, request
from service import user

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb',region_name='us-west-1')

@app.route("/")
def healthCheck():
    return "API reached successfully"

@app.route("/user",methods = ['POST','PUT','GET','DELETE'])
def addUser():
    table=dynamodb.Table('users')
    res_obj={}
    if request.method == 'POST':
        user.addUserMethod(table, request.body)
    elif request.method == 'PUT':
        user.updateUserMethod(table, request.args.get("user"),request.body)
    elif request.method == 'GET':
        if request.args.get("bulk") == "True":
            res_obj=user.getAllUsersMethod(table)
        else:
            res_obj=user.getUserMethod(table, request.args.get("user"))
    elif request.method == 'DELETE':
        user.deleteUserMethod()
    return res_obj

if __name__ == "__main__":
    app.run(debug=True)