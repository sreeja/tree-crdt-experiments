from flask import Flask
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
    return 'Hello world from tree experiment'
