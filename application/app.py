from flask import Flask, request
import os


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
    from messenger import write_message
    to = request.args.get('to', '')
    whoami = os.environ.get("WHOAMI")
    message = {"to": to, "payload": "Hello"}
    write_message(message)
    return f'Hello world from {whoami}'
