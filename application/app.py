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

from tree import Tree_CRDT, Tree_Opset, Tree_Globalock, Tree_Sublock

# latency configuration, 1,2,3
lc = int(os.environ.get("LC"))
# 0 for crdt, 1 for opsets, 2 for global lock, 3 for rw lock
exp = int(os.environ.get("EXP"))

memcache = FlaskPyMemcache()

def create_app():
    app = Flask(__name__)
    LC = {1:{
        "paris-paris": 0,
        "paris-bangalore": 0,
        "paris-newyork": 0,
        "bangalore-paris": 0,
        "bangalore-bangalore": 0,
        "bangalore-newyork": 0,
        "newyork-paris": 0,
        "newyork-bangalore": 0,
        "newyork-newyork": 0,
    },
    2: {
        "paris-paris": 0,
        "paris-bangalore": .144,
        "paris-newyork": .075,
        "bangalore-paris": .144,
        "bangalore-bangalore": 0,
        "bangalore-newyork": .215,
        "newyork-paris": .075,
        "newyork-bangalore": .215,
        "newyork-newyork": 0,
    }, 
    3: {
        "paris-paris": 0,
        "paris-bangalore": 1.44,
        "paris-newyork": 0.75,
        "bangalore-paris": 1.44,
        "bangalore-bangalore": 0,
        "bangalore-newyork": 2.15,
        "newyork-paris": 0.75,
        "newyork-bangalore": 2.15,
        "newyork-newyork": 0,
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

# def log_message(message):
#     msg = json.dumps(message.get("msg", ""))
#     f_to_write = os.path.join('/', 'usr', 'data', f'{whoami}.txt')
#     with open(f_to_write, "a") as f:
#         f.write(f"{msg}\n")

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

def get_logs():
    logs = []
    for each in replicas:
        f_to_read = os.path.join('/', 'usr', 'data', f'{each}.txt')
        with open(f_to_read, "r") as f:
            lines = f.readlines()
            for line in lines:
                logs += [json.loads(line)]
    return logs

def extract_ts(js):
    return js["ts"]

def order_logs(logs):
    ordered_logs = sorted(logs, key=extract_ts)
    if len(ordered_logs) > 0:
        last_ts = ordered_logs[len(ordered_logs) -1]['ts']
    else:
        last_ts = [0, 0, 0]
    return ordered_logs, last_ts

def rebuild_tree(logs, ts, tree):
    filtered_logs = [l for l in logs if l["ts"] <= ts]
    ordered_logs, last_ts = order_logs(filtered_logs)
    assert last_ts <= ts
    if exp == 0:
        # build CRDT tree
        tree = Tree_CRDT.construct_tree(filtered_logs, tree)
    elif exp == 1:
        # build opsets tree
        tree = Tree_Opset.construct_tree(ordered_logs, tree)
    elif exp == 2:
        # build tree with single lock
        tree = Tree_Globalock.construct_tree(filtered_logs, tree)
    else:
        # build tree with subtree locking
        tree = Tree_Sublock.construct_tree(filtered_logs, tree)
    return tree, last_ts

def equals(ts1, ts2):
    if len(ts1) != len(ts2):
        return False
    for each in range(len(ts1)):
        if ts1[each] != ts2[each]:
            return False
    return True

def get_tree(ts):
    cached_tree = memcache.client.get(whoami+'-tree')
    if cached_tree:
        stree = json.loads(cached_tree)
        if  equals(stree["ts"], ts):
            if exp == 0:
                tree = Tree_CRDT.deserialize(stree['tree'])
            elif exp ==1:
                tree = Tree_Opset.deserialize(stree['tree'])
            elif exp == 2:
                tree = Tree_Globalock.deserialize(stree['tree'])
            else:
                tree = Tree_Sublock.deserialize(stree['tree'])
            return tree
    logs = get_logs()
    tree, last_ts = rebuild_tree(logs, ts, None)
    return tree

def apply_log(log, tree, ts):
    if exp == 0:
        tree = Tree_CRDT.construct_tree([log], tree)
        memcache.client.set(whoami+'-tree', json.dumps({'ts':ts, 'tree':Tree_CRDT.serialize(tree)}))
    elif exp == 1:
        tree = Tree_Opset.construct_tree([log], tree)
        memcache.client.set(whoami+'-tree', json.dumps({'ts':ts, 'tree':Tree_Opset.serialize(tree)}))
    elif exp == 2:
        tree = Tree_Globalock.construct_tree([log], tree)
        memcache.client.set(whoami+'-tree', json.dumps({'ts':ts, 'tree':Tree_Globalock.serialize(tree)}))
    else:
        tree = Tree_Sublock.construct_tree([log], tree)
        memcache.client.set(whoami+'-tree', json.dumps({'ts':ts, 'tree':Tree_Sublock.serialize(tree)}))
    return tree

@app.route('/')
def hello_world():
    return f'Hello world from {whoami}'

@app.route('/add')
def add():
    replicaid = get_id(whoami)
    
    n = request.args.get('n', '')
    p = request.args.get('p', '')

    ts = get_latest_ts()
    tree = get_tree(ts)

    start_time = datetime.now()
    prep = tree.add_gen(n, p)
    ts[replicaid] += 1
    flag = False
    if prep:
        msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
    else:
        flag = True
        msg = prepare_message("skip", ts, [], whoami, [])
    message = {"to": whoami, "msg": msg}
    tree = apply_log(msg, tree, ts)
    log_time = datetime.now()
    update_ts_self(ts[replicaid])
    end_time = datetime.now()
    write_message(message)
    for each in [r for r in replicas if r != whoami]:
        message = {"to": each, "msg": msg}
        write_message(message)
    register_op(ts, start_time)
    # log_logtime(ts, log_time)
    acknowledge(ts, end_time)
    if not flag:
        return "done"
    else:
        return "skipped"

@app.route('/remove')
def remove():
    replicaid = get_id(whoami)
    
    n = request.args.get('n', '')
    p = request.args.get('p', '')

    ts = get_latest_ts()
    tree = get_tree(ts)

    start_time = datetime.now()
    prep = tree.remove_gen(n, p)
    ts[replicaid] += 1
    flag = False
    if prep:
        msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
    else:
        flag = True
        msg = prepare_message("skip", ts, [], whoami, [])    
    message = {"to": whoami, "msg": msg}
    tree = apply_log(msg, tree, ts)
    log_time = datetime.now()
    update_ts_self(ts[replicaid])
    end_time = datetime.now()
    write_message(message)
    for each in [r for r in replicas if r != whoami]:
        message = {"to": each, "msg": msg}
        write_message(message)
    register_op(ts, start_time)
    # log_logtime(ts, log_time)
    acknowledge(ts, end_time)
    if not flag:
        return "done"
    else:
        return "skipped"

@app.route('/move')
def move():
    replicaid = get_id(whoami)
    
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')

    if exp == 2:
        ts = get_latest_ts()
        tree = get_tree(ts)
        start_time = datetime.now()
        flag = False
        ts[replicaid] += 1
        prep = tree.move_gen(n, p, np)
        if prep:
            lock = zk.Lock('/global')
            simulate_latency()
            with lock:
                simulate_latency()
                ts = get_latest_ts()
                tree = get_tree(ts)
                ts[replicaid] += 1
                prep = tree.move_gen(n, p, np)
                if prep:
                    msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
                    message = {"to": whoami, "msg": msg}
                    tree = apply_log(msg, tree, ts)
                    log_time = datetime.now()
                    update_ts_self(ts[replicaid])
                    end_time = datetime.now()
                    write_message(message)
                    for each in [r for r in replicas if r != whoami]:
                        message = {"to": each, "msg": msg}
                        write_message(message)
                    register_op(ts, start_time)
                    log_logtime(ts, log_time)
                    acknowledge(ts, end_time)
                    simulate_latency()
                    return "done"
        msg = prepare_message("skip", ts, [], whoami, [])
        message = {"to": whoami, "msg": msg}
        tree = apply_log(msg, tree, ts)
        log_time = datetime.now()
        update_ts_self(ts[replicaid])
        end_time = datetime.now()
        write_message(message)
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)
        register_op(ts, start_time)
        log_logtime(ts, log_time)
        acknowledge(ts, end_time)
        return "skipped"

    elif exp == 3:
        # edit this code - should take a stable snapshot to work on and acquire locks
        ts = get_latest_ts()
        tree = get_tree(ts)
        start_time = datetime.now()
        prep = tree.move_gen(n, p, np)
        ts[replicaid] += 1
        if prep:
            locks = get_locks(n, prep[2])
            simulate_latency(len(locks))
            with ExitStack() as stack:
                l = [stack.enter_context(lock) for lock in locks]
                simulate_latency(len(locks))
                ts = get_latest_ts()
                tree = get_tree(ts)
                prep = tree.move_gen(n, p, np)
                ts[replicaid] += 1
                if prep:
                    msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
                    message = {"to": whoami, "msg": msg}
                    tree = apply_log(msg, tree, ts)
                    log_time = datetime.now()
                    update_ts_self(ts[replicaid])
                    end_time = datetime.now()
                    write_message(message)
                    for each in [r for r in replicas if r != whoami]:
                        message = {"to": each, "msg": msg}
                        write_message(message)
                    register_op(ts, start_time)
                    log_logtime(ts, log_time)
                    acknowledge(ts, end_time)
                    simulate_latency(len(locks))
                    return "done"
        msg = prepare_message("skip", ts, [], whoami, [])
        message = {"to": whoami, "msg": msg}
        tree = apply_log(msg, tree, ts)
        log_time = datetime.now()
        update_ts_self(ts[replicaid])
        end_time = datetime.now()
        write_message(message)
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)
        register_op(ts, start_time)
        log_logtime(ts, log_time)
        acknowledge(ts, end_time)
        return "skipped"
    else:
        ts = get_latest_ts()
        tree = get_tree(ts)
        start_time = datetime.now()
        prep = tree.move_gen(n, p, np)
        ts[replicaid] += 1
        if prep:
            msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
        else:
            flag = True
            msg = prepare_message("skip", ts, [], whoami, [])    
        message = {"to": whoami, "msg": msg}
        tree = apply_log(msg, tree, ts)
        log_time = datetime.now()
        update_ts_self(ts[replicaid])
        end_time = datetime.now()
        write_message(message)
        for each in [r for r in replicas if r != whoami]:
            message = {"to": each, "msg": msg}
            write_message(message)
        register_op(ts, start_time)
        # log_logtime(ts, log_time)
        acknowledge(ts, end_time)
        if flag:
                return "skipped"
        else:
            return "done"
