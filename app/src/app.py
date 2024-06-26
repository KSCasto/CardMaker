import boto3, json, os
from flask import Flask, request
from services.blueprints.users.users_blueprint import app as usersApp
from services.blueprints.cardMaker.cm_blueprint import CardMaker as cmBp
from services.utils.auth import authenticate
# from dotenv import dotenv_values as env

app = Flask(__name__)

app.config['CM_INPUT_FOLDER'] = '/app/services/blueprints/cardMaker/Input'
app.config['CM_OUTPUT_FOLDER'] = '/app/services/blueprints/cardMaker/Output'

app.register_blueprint(usersApp)
app.register_blueprint(cmBp)

# @app.before_request
# def pre_call():
#     token = request.headers.get('Authorization')
#     email = request.json.get('Email')
#     authenticate(email,token)

@app.route("/healthcheck")
def healthCheck():
    return "API reached successfully"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)