import os
import time

from flask import Flask, request
from messenger import write_message

import json
from multiprocessing import Process

from datetime import datetime

from kazoo.client import KazooClient

# 0 for crdt, 1 for opsets, 2 for global lock, 3 for rw lock
exp = 0

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET")
    app.config["latency_config"] = {
        "paris-bangalore": .144,
        "paris-newyork": .075,
        "bangalore-paris": .144,
        "bangalore-newyork": .215,
        "newyork-paris": .075,
        "newyork-bangalore": .215,
    }
    # app.config["latency_config"] = {
    #     "paris-bangalore": 1.44,
    #     "paris-newyork": 0.75,
    #     "bangalore-paris": 1.44,
    #     "bangalore-newyork": 2.15,
    #     "newyork-paris": 0.75,
    #     "newyork-bangalore": 2.15,
    # }
    # app.config["latency_config"] = {
    #     "paris-bangalore": 0,
    #     "paris-newyork": 0,
    #     "bangalore-paris": 0,
    #     "bangalore-newyork": 0,
    #     "newyork-paris": 0,
    #     "newyork-bangalore": 0,
    # }
    return app

app = create_app()

whoami = os.environ.get("WHOAMI")

ts = [0, 0, 0]
replicas = ['paris', 'bangalore','newyork']

zk = KazooClient(hosts='zookeeper:2181')
zk.start()
chairman = "paris"

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

def register_op():
    reg = json.dumps({"ts":ts, "time":str(datetime.now())})
    log_file = os.path.join('/', 'usr', 'data', 'register.txt')
    with open(log_file, "a") as l:
        l.write(f"{reg}\n")

def prepare_message(op, ts, args, replica, ca = []):
    return {"op": op, "ts":ts, "args": args, "replica": replica, "ca":ca}

def log_message(message):
    msg = json.dumps(message.get("msg", ""))
    msg_ts = message.get("msg", "").get("ts","")
    logging = json.dumps({"ts":msg_ts, "time":str(datetime.now())})
    # print(logging)
    log_file = os.path.join('/', 'usr', 'data', f'time{whoami}.txt')
    with open(log_file, "a") as l:
        l.write(f"{logging}\n")
    f_to_write = os.path.join('/', 'usr', 'data', f'{whoami}.txt')
    with open(f_to_write, "a") as f:
        f.write(f"{msg}\n")

def acknowledge():
    reg = json.dumps({"ts":ts, "time":str(datetime.now())})
    log_file = os.path.join('/', 'usr', 'data', 'done.txt')
    with open(log_file, "a") as l:
        l.write(f"{reg}\n")

# # the cost of lock acquisition is as per https://www.nuodb.com/techblog/distributed-transactional-locks
# # exclusive mode - 
# # -- requestor -> chairman (paris)
# # -- chairman(paris) -> all other nodes
# # -- all other nodes -> requestor
# # shared mode - 0
# def simulate_lock_time(latency_config):
#     chairman = "paris"
#     # -- requestor -> chairman (paris)
#     if whoami != chairman:
#         time.sleep(latency_config[whoami+'-'+chairman])
#     # -- chairman(paris) -> all other nodes
#     max_time = 0
#     for each in [r for r in replicas if r != chairman]:
#         max_time = max(max_time, latency_config[chairman+'-'+each])
#     time.sleep(max_time)
#     # -- all other nodes -> requestor
#     max_time = 0
#     for each in [r for r in replicas if r != whoami]:
#         max_time = max(max_time, latency_config[each+'-'+whoami])
#     time.sleep(max_time)

def acquire_locks():
    latency_config = app.config["latency_config"]
    if exp == 0:
        # crdt
        pass
    elif exp == 1:
        # opsets
        pass
    elif exp == 2:
        # global lock
        simulate_lock_time(latency_config)
    else:
        # rw lock
        simulate_lock_time()

def release_locks():
    if exp == 0:
        # crdt
        pass
    elif exp == 1:
        # opsets
        pass
    elif exp == 2:
        # global lock
        pass
    else:
        # rw lock
        pass

@app.route('/')
def hello_world():
    return f'Hello world from {whoami}'

# @app.route('/write')
# def write():
#     to = request.args.get('to', '')
#     message = {"to": to, "msg": "Hello"}
#     write_message(message)
#     return "done"

@app.route('/add')
def add():
    update_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    register_op()
    s = datetime.now()
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    msg = prepare_message("add", ts, {"n": n, "p": p}, whoami)
    message = {"to": whoami, "msg": msg}
    log_message(message)
    e = datetime.now()
    for each in [r for r in replicas if r != whoami]:
        message = {"to": each, "msg": msg}
        write_message(message)
    acknowledge()
    return str(e - s) #"done"

@app.route('/remove')
def remove():
    update_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    register_op()
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    msg = prepare_message("remove", ts, {"n": n, "p": p}, whoami)
    message = {"to": whoami, "msg": msg}
    log_message(message)
    for each in [r for r in replicas if r != whoami]:
        message = {"to": each, "msg": msg}
        write_message(message)
    acknowledge()
    return "done"

@app.route('/downmove')
def downmove():
    update_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    register_op()
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    ca = request.args.get('ca', '').split(',')
    # acquire lock if needed
    # acquire_locks()
    latency_config = app.config["latency_config"]
    if exp == 2:
        # global lock
        if whoami != chairman:
            time.sleep(latency_config[whoami+'-'+chairman])
        lock = zk.Lock('/lockpath', 'global')
        with lock:
            # print("with lock from "+whoami)
            msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
            message = {"to": whoami, "msg": msg}
            log_message(message)
            if whoami != chairman:
                time.sleep(latency_config[whoami+'-'+chairman]*2)
            for each in [r for r in replicas if r != whoami]:
                message = {"to": each, "msg": msg}
                write_message(message)
            # print("lock released from " + whoami)

    elif exp == 3:
        # rw lock
        if whoami != chairman:
            time.sleep(latency_config[whoami+'-'+chairman])
        wlock = zk.WriteLock('/lockpath', n)
        rlocks = [zk.ReadLock('/lockpath', a) for a in ca]
        from contextlib import ExitStack
        with rlocks and wlock: # ExitStack() as es:
            # print("got locks " +whoami, flush=True)
            msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
            message = {"to": whoami, "msg": msg}
            log_message(message)
            if whoami != chairman:
                time.sleep(latency_config[whoami+'-'+chairman]*2)
            for each in [r for r in replicas if r != whoami]:
                message = {"to": each, "msg": msg}
                write_message(message)
            # print("lock released from " + whoami, flush=True)

    else:
        # crdt/opsets
        msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
        message = {"to": whoami, "msg": msg}
        log_message(message)
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)

    # release lock if acquired
    # release_locks()
    acknowledge()
    return "done"

@app.route('/upmove')
def upmove():
    update_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    register_op()
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    ca = request.args.get('ca', '').split(',')
    # acquire lock if needed
    # acquire_locks()
    latency_config = app.config["latency_config"]
    if exp == 2:
        # global lock
        if whoami != chairman:
            time.sleep(latency_config[whoami+'-'+chairman])
        lock = zk.Lock('/lockpath', 'global')
        with lock:
            # print("with lock from "+whoami)
            msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
            message = {"to": whoami, "msg": msg}
            log_message(message)
            if whoami != chairman:
                time.sleep(latency_config[whoami+'-'+chairman]*2)
            for each in [r for r in replicas if r != whoami]:
                message = {"to": each, "msg": msg}
                write_message(message)

    elif exp == 3:
        # rw lock
        if whoami != chairman:
            time.sleep(latency_config[whoami+'-'+chairman])
        wlock = zk.WriteLock('/lockpath', n)
        rlocks = [zk.ReadLock('/lockpath', a) for a in ca]
        from contextlib import ExitStack
        with rlocks and wlock: # ExitStack() as es:
            # print("got locks " +whoami, flush=True)
            msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
            message = {"to": whoami, "msg": msg}
            log_message(message)
            if whoami != chairman:
                time.sleep(latency_config[whoami+'-'+chairman]*2)
            for each in [r for r in replicas if r != whoami]:
                message = {"to": each, "msg": msg}
                write_message(message)

    else:
        # crdt/opsets
        msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
        message = {"to": whoami, "msg": msg}
        log_message(message)
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)

    # release lock if acquired
    # release_locks()
    acknowledge()
    return "done"

