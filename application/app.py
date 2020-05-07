import os

from flask import Flask, request
from messenger import write_message

import json
from multiprocessing import Process


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET")
    app.config["RABBIT_URI"] = "%s/vaypa" % os.environ.get(
        "MONGO_URL", "mongodb://localhost:27017")
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
                    replica = msg["replica"]
                    replicaid = get_id(each)
                    ts[replicaid] = log_ts[replicaid]
                    print("log received until " + str(ts))

def prepare_message(op, ts, args, replica, ca = []):
    return {"op": op, "ts":ts, "args": args, "replica": replica, "ca":ca}

def log_message(message):
    msg = json.dumps(message.get("msg", ""))
    f_to_write = os.path.join('/', 'usr', 'data', f'{whoami}.txt')
    with open(f_to_write, "a") as f:
        f.write(f"{msg}\n")

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
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    msg = prepare_message("add", ts, {"n": n, "p": p}, whoami)
    message = {"to": whoami, "msg": msg}
    log_message(message)
    for each in [r for r in replicas if r != whoami]:
        message = {"to": each, "msg": msg}
        write_message(message)
    return "done"

@app.route('/remove')
def remove():
    update_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    msg = prepare_message("remove", ts, {"n": n, "p": p}, whoami)
    message = {"to": whoami, "msg": msg}
    log_message(message)
    for each in replicas:
        message = {"to": each, "msg": msg}
        write_message(message)
    return "done"

@app.route('/downmove')
def downmove():
    update_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    ca = request.args.get('ca', '').split(',')
    msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
    message = {"to": whoami, "msg": msg}
    log_message(message)
    for each in replicas:
        message = {"to": each, "msg": msg}
        write_message(message)
    return "done"

@app.route('/upmove')
def upmove():
    update_ts()
    whoami = os.environ.get("WHOAMI")
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    ca = request.args.get('ca', '').split(',')
    msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
    message = {"to": whoami, "msg": msg}
    log_message(message)
    for each in replicas:
        message = {"to": each, "msg": msg}
        write_message(message)
    return "done"

