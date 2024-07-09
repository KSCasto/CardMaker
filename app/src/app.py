import boto3, json, os
from flask import Flask, request, jsonify
from services.blueprints.users.users_blueprint import app as usersApp
from services.blueprints.cardMaker.cm_blueprint import CardMaker as cmBp
from services.utils.auth import authenticate
from dotenv import load_dotenv
import logging


app = Flask(__name__)

# Absolute paths in Docker
app.config['CM_INPUT_FOLDER'] = '/app/services/blueprints/cardMaker/Input'
app.config['CM_OUTPUT_FOLDER'] = '/app/services/blueprints/cardMaker/Output'

# Relative paths for local dev
# app.config['CM_INPUT_FOLDER'] = './services/blueprints/cardMaker/Input'
# app.config['CM_OUTPUT_FOLDER'] = './services/blueprints/cardMaker/Output'

app.register_blueprint(usersApp)
app.register_blueprint(cmBp)

@app.before_request
def pre_call():
    token = request.headers.get('Authorization')
    uid = request.headers.get('UID')

    if token and token.startswith("Bearer "):
        token = token[len("Bearer "):]

    logging.info(f"Authenticating for user {uid}...")
    # authenticated=authenticate(uid,token)
    logging.info(f"Authenticated")

    # if not authenticated:
        # logging.warning("Unauthorized access attempt")
        # return jsonify({'error': 'Unauthorized access'}), 401

@app.route("/healthcheck")
def healthCheck():
    return "API reached successfully"

if __name__ == "__main__":
    load_dotenv('/app/.env')
    app.run(host=os.environ.get("FLASK_RUN_HOST"), port=5000)