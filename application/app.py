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

ts = [0, 0, 0]

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

@app.route('/add')
def add():
    to = request.args.get('to', '')
    whoami = os.environ.get("WHOAMI")
    replicaid = 0
    if whoami == "bangalore":
        replicaid = 1
    elif whoami == "newyork":
        replicaid = 2
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    # ["add", ts, [parent, node, replica], []]
    message = {"to": to, "msg": {"op": "add", "ts":ts, "args": {"n": n, "p": p, "replica": whoami}, "ca":[]}}
    write_message(message)
    return "done"

@app.route('/remove')
def remove():
    to = request.args.get('to', '')
    whoami = os.environ.get("WHOAMI")
    replicaid = 0
    if whoami == "bangalore":
        replicaid = 1
    elif whoami == "newyork":
        replicaid = 2
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    # ["remove", ts, [parent, node, replica], []]]
    message = {"to": to, "msg": {"op": "remove", "ts":ts, "args": {"n": n, "p": p, "replica": whoami}, "ca":[]}}
    write_message(message)
    return "done"

@app.route('/downmove')
def downmove():
    to = request.args.get('to', '')
    whoami = os.environ.get("WHOAMI")
    replicaid = 0
    if whoami == "bangalore":
        replicaid = 1
    elif whoami == "newyork":
        replicaid = 2
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    # ["downmove", ts, [parent, node, new_parent, replica], self.get_critical_ancestors(node, new_parent)]
    message = {"to": to, "msg": {"op": "downmove", "ts":ts, "args": {"n": n, "p": p, "np": np, "replica": whoami}, "ca":["a", "aa"]}}
    write_message(message)
    return "done"

@app.route('/upmove')
def upmove():
    to = request.args.get('to', '')
    whoami = os.environ.get("WHOAMI")
    replicaid = 0
    if whoami == "bangalore":
        replicaid = 1
    elif whoami == "newyork":
        replicaid = 2
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    # ["downmove", ts, [parent, node, new_parent, replica], self.get_critical_ancestors(node, new_parent)]
    message = {"to": to, "msg": {"op": "upmove", "ts":ts, "args": {"n": n, "p": p, "np": np, "replica": whoami}, "ca":["a", "aa"]}}
    write_message(message)
    return "done"

