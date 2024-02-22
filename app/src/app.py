import boto3, json, os
from flask import Flask, request
from services.blueprints.users.users_blueprint import app as usersApp
from services.blueprints.cardMaker.cm_blueprint import CardMaker as cmBp
# from dotenv import dotenv_values as env

app = Flask(__name__)

app.config['CM_INPUT_FOLDER'] = '/app/services/blueprints/cardMaker/Input'
app.config['CM_OUTPUT_FOLDER'] = '/app/services/blueprints/cardMaker/Output'

app.register_blueprint(usersApp)
app.register_blueprint(cmBp)

@app.route("/healthcheck")
def healthCheck():
    return "API reached successfully"

if __name__ == "__main__":
    app.run(debug=True, host=os.environ("FLASK_RUN_HOST"), port=5000)