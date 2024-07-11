import sys
from flask import Flask, Blueprint, request, jsonify
import boto3
from botocore.config import Config
from services.blueprints.users.utils import user
from services.blueprints.users.utils import user_preferences
from services.utils import db

app = Blueprint('users', __name__)

boto3_config = Config(
    max_pool_connections=100,
    connect_timeout=5,         # Connection timeout in seconds
    read_timeout=5,            # Read timeout in seconds
    retries={'max_attempts': 3}  # Number of retry attempts
)
dynamodb = boto3.resource('dynamodb', config=boto3_config)


def handle_response(func):
    try:
        result = func()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/user", methods=['POST', 'PUT', 'GET', 'DELETE'])
def userCRUD():
    def execute():
        # dynamodb = db.connect()
        table = dynamodb.Table('users')
        
        if request.method == 'POST':
            user_data = request.json
            if "email" not in user_data:
                return {"success": False, "error": "Missing key 'email' in body"}
            email = user_data["email"]
            user.addUserMethod(table, email)
            return user.getUserMethod(table, email) 
        elif request.method == 'PUT':
            return user.updateUserMethod(table, request.args.get("user"), request.json)
        elif request.method == 'GET':
            if request.args.get("user"):
                return user.getUserMethod(table, request.args.get("user"))
            else:
                return user.getAllUsersMethod(table)
        elif request.method == 'DELETE':
            user.deleteUserMethod(table, request.args.get("user"))
            return {"success": True, "message": f"User {request.args.get('user')} deleted"}
    return handle_response(execute)

@app.route("/user-prefs", methods=['POST', 'PUT', 'GET', 'DELETE'])
def userPrefsCRUD():
    def execute():
        # dynamodb = db.connect()
        table = dynamodb.Table('user_preferences')
        
        if request.method == 'POST':
            user_data = request.json
            if "user_id" not in user_data:
                return {"success": False, "error": "Missing key 'user_id' in body"}
            user_id = user_data["user_id"]
            user_preferences.addProfile(table, user_id)
            return user_preferences.getProfile(table, user_id)
        
        elif request.method == 'PUT':
            return user_preferences.updateProfile(table, request.args.get("user"), request.args.get("profile"), request.json)
        
        elif request.method == 'GET':
            if request.args.get("profile"):
                return user_preferences.getProfile(table, request.args.get("user"), request.args.get("profile"))
            elif request.args.get("user-profiles"):
                return user_preferences.getAllUserProfiles(table, request.args.get("user-profiles"))
            elif request.args.get("all-profiles"):
                return user_preferences.getAllProfiles(table)
        
        elif request.method == 'DELETE':
            user_preferences.deleteProfile(table, request.args.get("user"))
            return {"success": True, "message": f"User {request.args.get('user')} deleted"}
    
    return handle_response(execute)