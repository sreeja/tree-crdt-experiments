import os

from flask import Flask, request
from messenger import write_message

import json

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET")
    app.config["RABBIT_URI"] = "%s/vaypa" % os.environ.get(
        "MONGO_URL", "mongodb://localhost:27017")
    # app.register_blueprint(vaypa_apis, url_prefix="/api")
    return app

app = create_app()

whoami = os.environ.get("WHOAMI")

ts = [0, 0, 0]
replicas = ['paris', 'bangalore','newyork']

def get_id(replica):
    return replicas.index(replica)

def update_ts():
    for each in replicas:
        if each != whoami:
            f_to_read = os.path.join('/', 'usr', 'data', f'{each}.txt')
            with open(f_to_read, 'r') as f:
                lines = f.read().splitlines()
                if lines:
                    last_line = lines[-1]
                    msg = json.loads(last_line)
                    log_ts = msg["ts"]
                    print("log ts" + str(log_ts))
                    replica = msg["args"]["replica"]
                    replicaid = get_id(each)
                    print("replica id" + str(replicaid))
                    ts[replicaid] = log_ts[replicaid]
                    print("log received until " + str(ts))

@app.route('/')
def hello_world():
    return f'Hello world from {whoami}'

@app.route('/write')
def write():
    to = request.args.get('to', '')
    message = {"to": to, "msg": "Hello"}
    write_message(message)
    return "done"

@app.route('/add')
def add():
    update_ts()
    to = request.args.get('to', '')
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    # ["add", ts, [parent, node, replica], []]
    message = {"to": to, "msg": {"op": "add", "ts":ts, "args": {"n": n, "p": p, "replica": whoami}, "ca":[]}}
    write_message(message)
    return "done"

@app.route('/remove')
def remove():
    update_ts()
    to = request.args.get('to', '')
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    # ["remove", ts, [parent, node, replica], []]]
    message = {"to": to, "msg": {"op": "remove", "ts":ts, "args": {"n": n, "p": p, "replica": whoami}, "ca":[]}}
    write_message(message)
    return "done"

@app.route('/downmove')
def downmove():
    update_ts()
    to = request.args.get('to', '')
    replicaid = get_id(whoami)
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
    update_ts()
    to = request.args.get('to', '')
    whoami = os.environ.get("WHOAMI")
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    # ["downmove", ts, [parent, node, new_parent, replica], self.get_critical_ancestors(node, new_parent)]
    message = {"to": to, "msg": {"op": "upmove", "ts":ts, "args": {"n": n, "p": p, "np": np, "replica": whoami}, "ca":["a", "aa"]}}
    write_message(message)
    return "done"

