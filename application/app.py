import os
import time

from flask import Flask, request
from messenger import write_message

import json
from multiprocessing import Process

from datetime import datetime

from kazoo.client import KazooClient
from flask_pymemcache import FlaskPyMemcache

from contextlib import ExitStack

# latency configuration, 1,2,3
lc = int(os.environ.get("LC"))
# 0 for crdt, 1 for opsets, 2 for global lock, 3 for rw lock
exp = int(os.environ.get("EXP"))

memcache = FlaskPyMemcache()

def create_app():
    app = Flask(__name__)
    # app.secret_key = os.environ.get("SESSION_SECRET")
    LC = {1:{
        "paris-bangalore": 0,
        "paris-newyork": 0,
        "bangalore-paris": 0,
        "bangalore-newyork": 0,
        "newyork-paris": 0,
        "newyork-bangalore": 0,
    },
    2: {
        "paris-bangalore": .144,
        "paris-newyork": .075,
        "bangalore-paris": .144,
        "bangalore-newyork": .215,
        "newyork-paris": .075,
        "newyork-bangalore": .215,
    }, 
    3: {
        "paris-bangalore": 1.44,
        "paris-newyork": 0.75,
        "bangalore-paris": 1.44,
        "bangalore-newyork": 2.15,
        "newyork-paris": 0.75,
        "newyork-bangalore": 2.15,
    },
    }
    app.config["latency_config"] = LC[lc]
    app.config["PYMEMCACHE"] = {
        'server': ('cache', 11211),
    }
    memcache.init_app(app)
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

def get_latest_ts():
    ts = [0, 0, 0]
    for each in replicas:
        val = memcache.client.get(each+'-'+whoami)
        if val:
            ts[replicas.index(each)] = int(val)
    return ts

def update_ts_self(t):
    memcache.client.set(whoami+'-'+whoami, t)

def register_op(ts, timestamp):
    reg = json.dumps({"ts":ts, "time":str(timestamp)})
    log_file = os.path.join('/', 'usr', 'data', 'register.txt')
    with open(log_file, "a") as l:
        l.write(f"{reg}\n")

def prepare_message(op, ts, args, replica, ca = []):
    return {"op": op, "ts":ts, "args": args, "replica": replica, "ca":ca}

def log_message(message):
    msg = json.dumps(message.get("msg", ""))
    f_to_write = os.path.join('/', 'usr', 'data', f'{whoami}.txt')
    with open(f_to_write, "a") as f:
        f.write(f"{msg}\n")

def log_logtime(ts, timestamp):
    logging = json.dumps({"ts":ts, "time":str(timestamp)})
    log_file = os.path.join('/', 'usr', 'data', f'time{whoami}.txt')
    with open(log_file, "a") as l:
        l.write(f"{logging}\n")

def acknowledge(ts, timestamp):
    reg = json.dumps({"ts":ts, "time":str(timestamp)})
    log_file = os.path.join('/', 'usr', 'data', 'done.txt')
    with open(log_file, "a") as l:
        l.write(f"{reg}\n")

def simulate_latency(n=1):
    latency_config = app.config["latency_config"]
    avg = sum(latency_config.values()) / len(latency_config.values())
    time.sleep(avg * n)
    # if whoami != chairman:
    #     # for now simulating only 1x latency, assuming some lock service can process list of locks
    #     time.sleep(latency_config[whoami+'-'+chairman] * n)

def get_locks(n, ca):
    w = n
    l = sorted([n] + ca)
    locks = []
    for each in l:
        if each == w:
            locks += [zk.WriteLock('/'+each)]
        else:
            locks += [zk.ReadLock('/'+each)]
    return locks

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
    start_time = datetime.now()
    ts = get_latest_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    msg = prepare_message("add", ts, {"n": n, "p": p}, whoami)
    message = {"to": whoami, "msg": msg}
    log_message(message)
    log_time = datetime.now()
    update_ts_self(ts[replicaid])
    end_time = datetime.now()
    for each in [r for r in replicas if r != whoami]:
        message = {"to": each, "msg": msg}
        write_message(message)
    register_op(ts, start_time)
    log_logtime(ts, log_time)
    acknowledge(ts, end_time)
    return "done"

@app.route('/remove')
def remove():
    start_time = datetime.now()
    ts = get_latest_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    msg = prepare_message("remove", ts, {"n": n, "p": p}, whoami)
    message = {"to": whoami, "msg": msg}
    log_message(message)
    log_time = datetime.now()
    update_ts_self(ts[replicaid])
    end_time = datetime.now()
    for each in [r for r in replicas if r != whoami]:
        message = {"to": each, "msg": msg}
        write_message(message)
    register_op(ts, start_time)
    log_logtime(ts, end_time)
    acknowledge(ts, end_time)
    return "done"

@app.route('/downmove')
def downmove():
    start_time = datetime.now()
    ts = get_latest_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    ca = request.args.get('ca', '').split(',')
    # acquire lock if needed
    # acquire_locks()
    if exp == 2:
        # global lock
        simulate_latency()
        lock = zk.Lock('/lockpath', 'global')
        with lock:
            # print("with lock from "+whoami)
            simulate_latency()
            msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
            message = {"to": whoami, "msg": msg}
            log_message(message)
            log_time = datetime.now()
            update_ts_self(ts[replicaid])
            end_time = datetime.now()
            simulate_latency()
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)
            # print("lock released from " + whoami)

    elif exp == 3:
        # rw lock
        locks = get_locks(n, ca)
        # ideally it should happen with a single readlock and write lock, efficiently managed by the application
        # for sake of simplicity, we just consider all read locks acquired in a single go
        simulate_latency(len(locks))
        with ExitStack() as stack:
            l = [stack.enter_context(lock) for lock in locks]
            # with rlocks and wlock: 
            # print("got locks " +whoami, flush=True)
            simulate_latency(len(locks))
            msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
            message = {"to": whoami, "msg": msg}
            log_message(message)
            log_time = datetime.now()
            update_ts_self(ts[replicaid])
            end_time = datetime.now()
            simulate_latency(len(locks))
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)
            # print("lock released from " + whoami, flush=True)

    else:
        # crdt/opsets
        msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
        message = {"to": whoami, "msg": msg}
        log_message(message)
        log_time = datetime.now()
        update_ts_self(ts[replicaid])
        end_time = datetime.now()
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)

    # release lock if acquired
    # release_locks()
    register_op(ts, start_time)
    log_logtime(ts, log_time)
    acknowledge(ts, end_time)
    return "done"

@app.route('/upmove')
def upmove():
    start_time = datetime.now()
    ts = get_latest_ts()
    replicaid = get_id(whoami)
    ts[replicaid] += 1
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')
    ca = request.args.get('ca', '').split(',')
    # acquire lock if needed
    # acquire_locks()
    if exp == 2:
        # global lock
        simulate_latency()
        lock = zk.Lock('/lockpath', 'global')
        with lock:
            # print("with lock from "+whoami)
            simulate_latency()
            msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
            message = {"to": whoami, "msg": msg}
            log_message(message)
            log_time = datetime.now()
            update_ts_self(ts[replicaid])
            end_time = datetime.now()
            simulate_latency()
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)

    elif exp == 3:
        # rw lock
        locks = get_locks(n, ca)
        simulate_latency(len(locks))
        with ExitStack() as stack:
            l = [stack.enter_context(lock) for lock in locks]
            # with rlocks and wlock: 
            # print("got locks " +whoami, flush=True)
            simulate_latency(len(locks))
            msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
            message = {"to": whoami, "msg": msg}
            log_message(message)
            log_time = datetime.now()
            update_ts_self(ts[replicaid])
            end_time = datetime.now()
            simulate_latency(len(locks))
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)

    else:
        # crdt/opsets
        msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
        message = {"to": whoami, "msg": msg}
        log_message(message)
        log_time = datetime.now()
        update_ts_self(ts[replicaid])
        end_time = datetime.now()
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)

    # release lock if acquired
    # release_locks()
    register_op(ts, start_time)
    log_logtime(ts, end_time)
    acknowledge(ts, end_time)
    return "done"

