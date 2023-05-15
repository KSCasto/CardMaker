import boto3, json
from flask import Flask, request
from services.blueprints.users.users_blueprint import app as usersApp

app = Flask(__name__)
app.register_blueprint(usersApp)

@app.route("/")
def healthCheck():
    return "API reached successfully"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)