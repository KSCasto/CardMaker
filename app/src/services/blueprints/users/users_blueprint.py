import sys
#This import is from the perspective of app.py in the app parent directory
from services.blueprints.users.utils import user
from services.blueprints.users.utils import user_preferences

from flask import Flask,Blueprint,request,jsonify
from services.utils import db

app = Blueprint('users',__name__)

@app.route("/user",methods = ['POST','PUT','GET','DELETE'])
def userCRUD():
    dynamodb=db.connect()
    table=dynamodb.Table('users')
    res_obj={}
    if request.method == 'POST':
        user_data=request.json
        if ("email" in user_data):
            email=user_data["email"]
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

@app.route("/user-prefs", methods = ['POST','PUT','GET','DELETE'])
def userPrefsCRUD():
    dynamodb=db.connect()
    table=dynamodb.Table('user_preferences')
    res_obj={}
    if request.method == 'POST':
        user_data=request.json
        if ("user_id" in user_data):
            user_id=user_data["user_id"]
            user_preferences.addProfile(table, user_id)
            res_obj=user_preferences.getProfile(table,user_id)
        else:
            res_obj="Missing key 'user_id' in body"
    elif request.method == 'PUT':
        res_obj=user_preferences.updateProfile(table, request.args.get("user"), request.args.get("profile"),request.json)
    elif request.method == 'GET':
        if request.args.get("profile"):
            res_obj=user_preferences.getProfile(table, request.args.get("user"),request.args.get("profile"))
        elif request.args.get("user-profiles"):
            res_obj=user_preferences.getAllUserProfiles(table, request.args.get("user-profiles"))
        elif request.args.get("all-profiles"):
            res_obj=user_preferences.getAllProfiles(table)
    elif request.method == 'DELETE':
        user_preferences.deleteProfile(table,request.args.get("user"))
        res_obj=f"User {request.args.get('user')} deleted"
    return jsonify(res_obj)