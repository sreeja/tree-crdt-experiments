import os

from flask import Flask, request
from messenger import write_message

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET")
    app.config["RABBIT_URI"] = "%s/vaypa" % os.environ.get(
        "MONGO_URL", "mongodb://localhost:27017")
    # app.register_blueprint(vaypa_apis, url_prefix="/api")
    return app


app = create_app()


@app.route('/')
def hello_world():
    whoami = os.environ.get("WHOAMI")
    return f'Hello world from {whoami}'


@app.route('/write')
def write():
    to = request.args.get('to', '')
    message = {"to": to, "msg": "Hello"}
    write_message(message)
    return "done"
