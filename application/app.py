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

import sys
sys.path.insert(1,'/Users/snair/works/tree-crdt-experiments')
from trees.tree import Tree_CRDT, Tree_Opset, Tree_Globalock, Tree_Sublock

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
        "bangalore-bangalore": 0
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
        "bangalore-bangalore": 0
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
        "bangalore-bangalore": 0
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
    return js['ts']

def order_logs(logs):
    ordered_logs = sorted(logs, key=extract_ts)
    return ordered_logs, ordered_logs[len(ordered_logs) -1]['ts']

def rebuild_tree(logs, tree):
    ordered_logs, last_ts = order_logs(logs)
    if exp == 0:
        # build CRDT tree
        stree = Tree_CRDT.serialize(Tree_CRDT.construct_tree(logs, tree))
    elif exp == 1:
        # build opsets tree
        stree = Tree_Opset.serialize(Tree_Opset.construct_tree(ordered_logs, tree))
    elif exp == 2:
        # build tree with single lock
        stree = Tree_Globalock.serialize(Tree_Globalock.construct_tree(logs, tree))
    else:
        # build tree with subtree locking
        stree = Tree_Sublock.serialize(Tree_Sublock.construct_tree(logs, tree))
    return stree, last_ts

def get_tree(ts):
    stree = memcache.client.get(whoami+'-tree')
    if stree['ts'] == ts:
        if exp == 0:
            tree = Tree_CRDT.deserialize(stree['tree'])
        elif exp ==1:
            tree = Tree_Opset.deserialize(stree['tree'])
        elif exp == 2:
            tree = Tree_Globalock.deserialize(stree['tree'])
        else:
            tree = Tree_Sublock.deserialize(stree['tree'])
    else:
        logs = get_logs()
        tree, last_ts = rebuild_tree(logs, None)
    return tree

@app.route('/')
def hello_world():
    return f'Hello world from {whoami}'

@app.route('/add')
def add():
    # start_time = datetime.now()
    # ts = get_latest_ts()
    # replicaid = get_id(whoami)
    # ts[replicaid] += 1
    # n = request.args.get('n', '')
    # p = request.args.get('p', '')
    # msg = prepare_message("add", ts, {"n": n, "p": p}, whoami)
    # message = {"to": whoami, "msg": msg}
    # log_time = datetime.now()
    # update_ts_self(ts[replicaid])
    # end_time = datetime.now()
    # write_message(message)
    # for each in [r for r in replicas if r != whoami]:
    #     message = {"to": each, "msg": msg}
    #     write_message(message)
    # register_op(ts, start_time)
    # log_logtime(ts, log_time)
    # acknowledge(ts, end_time)
    # return "done"

    start_time = datetime.now()
    replicaid = get_id(whoami)
    
    n = request.args.get('n', '')
    p = request.args.get('p', '')

    ts = get_latest_ts()
    tree = get_tree(ts)
    prep = tree.add_gen(n, p)
    if prep:
        ts[replicaid] += 1
        msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
        message = {"to": whoami, "msg": msg}
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
        return "done"
    else:
        return "skipped"

@app.route('/remove')
def remove():
    # start_time = datetime.now()
    # ts = get_latest_ts()
    # replicaid = get_id(whoami)
    # ts[replicaid] += 1
    # n = request.args.get('n', '')
    # p = request.args.get('p', '')
    # msg = prepare_message("remove", ts, {"n": n, "p": p}, whoami)
    # message = {"to": whoami, "msg": msg}
    # log_time = datetime.now()
    # update_ts_self(ts[replicaid])
    # end_time = datetime.now()
    # write_message(message)
    # for each in [r for r in replicas if r != whoami]:
    #     message = {"to": each, "msg": msg}
    #     write_message(message)
    # register_op(ts, start_time)
    # log_logtime(ts, log_time)
    # acknowledge(ts, end_time)
    # return "done"

    start_time = datetime.now()
    replicaid = get_id(whoami)
    
    n = request.args.get('n', '')
    p = request.args.get('p', '')

    ts = get_latest_ts()
    tree = get_tree(ts)
    prep = tree.remove_gen(n, p)
    if prep:
        ts[replicaid] += 1
        msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
        message = {"to": whoami, "msg": msg}
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
        return "done"
    else:
        return "skipped"

@app.route('/move')
def move():
    start_time = datetime.now()
    replicaid = get_id(whoami)
    
    n = request.args.get('n', '')
    p = request.args.get('p', '')
    np = request.args.get('np', '')

    ts = get_latest_ts()
    tree = get_tree(ts)
    prep = tree.move_gen(n, p)
    if prep:
        ts[replicaid] += 1
        if exp == 2:
            simulate_latency()
            lock = zk.Lock('/global')
            with lock:
                simulate_latency()
                ts = get_latest_ts()
                tree = get_tree(ts)
                prep = tree.move_gen(n, p)
                if prep:
                    msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
                    message = {"to": whoami, "msg": msg}
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
                    return "done"
        if exp == 3:
            locks = get_locks(n, ca)
            simulate_latency(len(locks))
            with ExitStack() as stack:
                l = [stack.enter_context(lock) for lock in locks]
                simulate_latency(len(locks))
                ts = get_latest_ts()
                tree = get_tree(ts)
                prep = tree.move_gen(n, p)
                if prep:
                    msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
                    message = {"to": whoami, "msg": msg}
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
                    return "done"
        else:
            msg = prepare_message(prep[0], ts, prep[1], whoami, prep[2])
            message = {"to": whoami, "msg": msg}
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
            return "done"
    else:
        return "skipped"


# @app.route('/downmove')
# def downmove():
#     start_time = datetime.now()
#     ts = get_latest_ts()
#     replicaid = get_id(whoami)
#     ts[replicaid] += 1
#     n = request.args.get('n', '')
#     p = request.args.get('p', '')
#     np = request.args.get('np', '')
#     ca = request.args.get('ca', '').split(',')
#     if exp == 2:
#         # global lock
#         simulate_latency()
#         lock = zk.Lock('/lockpath', 'global')
#         with lock:
#             simulate_latency()
#             msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
#             message = {"to": whoami, "msg": msg}
#             log_time = datetime.now()
#             update_ts_self(ts[replicaid])
#             end_time = datetime.now()
#             write_message(message)
#             simulate_latency()
#         for each in [r for r in replicas if r != whoami]:
#             message = {"to": each, "msg": msg}
#             write_message(message)

#     elif exp == 3:
#         # rw lock
#         locks = get_locks(n, ca)
#         simulate_latency(len(locks))
#         with ExitStack() as stack:
#             l = [stack.enter_context(lock) for lock in locks]
#             simulate_latency(len(locks))
#             msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
#             message = {"to": whoami, "msg": msg}
#             log_time = datetime.now()
#             update_ts_self(ts[replicaid])
#             end_time = datetime.now()
#             write_message(message)
#             simulate_latency(len(locks))
#         for each in [r for r in replicas if r != whoami]:
#             message = {"to": each, "msg": msg}
#             write_message(message)

#     else:
#         # crdt/opsets
#         msg = prepare_message("downmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
#         message = {"to": whoami, "msg": msg}
#         log_time = datetime.now()
#         update_ts_self(ts[replicaid])
#         end_time = datetime.now()
#         write_message(message)
#         for each in [r for r in replicas if r != whoami]:
#             message = {"to": each, "msg": msg}
#             write_message(message)

#     register_op(ts, start_time)
#     log_logtime(ts, log_time)
#     acknowledge(ts, end_time)
#     return "done"

# @app.route('/upmove')
# def upmove():
#     start_time = datetime.now()
#     ts = get_latest_ts()
#     replicaid = get_id(whoami)
#     ts[replicaid] += 1
#     n = request.args.get('n', '')
#     p = request.args.get('p', '')
#     np = request.args.get('np', '')
#     ca = request.args.get('ca', '').split(',')
#     if exp == 2:
#         # global lock
#         simulate_latency()
#         lock = zk.Lock('/lockpath', 'global')
#         with lock:
#             simulate_latency()
#             msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
#             message = {"to": whoami, "msg": msg}
#             log_time = datetime.now()
#             update_ts_self(ts[replicaid])
#             end_time = datetime.now()
#             write_message(message)
#             simulate_latency()
#         for each in [r for r in replicas if r != whoami]:
#             message = {"to": each, "msg": msg}
#             write_message(message)

#     elif exp == 3:
#         # rw lock
#         locks = get_locks(n, ca)
#         simulate_latency(len(locks))
#         with ExitStack() as stack:
#             l = [stack.enter_context(lock) for lock in locks]
#             simulate_latency(len(locks))
#             msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
#             message = {"to": whoami, "msg": msg}
#             log_time = datetime.now()
#             update_ts_self(ts[replicaid])
#             end_time = datetime.now()
#             write_message(message)
#             simulate_latency(len(locks))
#         for each in [r for r in replicas if r != whoami]:
#             message = {"to": each, "msg": msg}
#             write_message(message)

#     else:
#         # crdt/opsets
#         msg = prepare_message("upmove", ts, {"n": n, "p": p, "np": np}, whoami, ca)
#         message = {"to": whoami, "msg": msg}
#         log_time = datetime.now()
#         update_ts_self(ts[replicaid])
#         end_time = datetime.now()
#         write_message(message)
#         for each in [r for r in replicas if r != whoami]:
#             message = {"to": each, "msg": msg}
#             write_message(message)

#     register_op(ts, start_time)
#     log_logtime(ts, log_time)
#     acknowledge(ts, end_time)
#     return "done"

