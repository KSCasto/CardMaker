import boto3, json, os
from flask import Flask, request
from services.blueprints.users.users_blueprint import app as usersApp
# from dotenv import dotenv_values as env

app = Flask(__name__)
app.register_blueprint(usersApp)

@app.route("/healthcheck")
def healthCheck():
    return "API reached successfully"

if __name__ == "__main__":
    app.run(debug=True, host=os.environ("FLASK_RUN_HOST"), port=5000)