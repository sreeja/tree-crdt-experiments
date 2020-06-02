import time
import os
import pika
import json
from datetime import datetime
from pymemcache.client.base import Client

from tree import Tree_CRDT, Tree_Opset, Tree_Globalock, Tree_Sublock

time.sleep(30)  # A hack for rabbitmq to start
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='messenger'))
channel = connection.channel()

queue_to_cosume = os.environ.get("WHOAMI")
print(queue_to_cosume)
channel.queue_declare(queue=queue_to_cosume, durable=True)

replicas = ['paris', 'bangalore','newyork']
cache_client = Client(('cache', 11211))

exp = int(os.environ.get("EXP"))

def get_latest_ts():
    ts = [0, 0, 0]
    for each in replicas:
        val = cache_client.get(each+'-'+queue_to_cosume)
        if val:
            ts[replicas.index(each)] = int(val)
    return ts

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
    # print(js, type(js), flush=True)
    return js["ts"]

def order_logs(logs):
    ordered_logs = sorted(logs, key=extract_ts)
    return ordered_logs, ordered_logs[len(ordered_logs) -1]["ts"]

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

def apply_log(log):
    c = cache_client.get(queue_to_cosume+'-tree')
    if c:
        cached_tree = json.loads(c)
        latest_ts = get_latest_ts()
        if cached_tree and latest_ts == cached_tree['ts']:
            if exp == 0:
                # build CRDT tree
                tree = Tree_CRDT.deserialize(cached_tree['tree'])
            elif exp == 1:
                # build opsets tree
                tree = Tree_Opset.deserialize(cached_tree['tree'])
            elif exp == 2:
                # build tree with single lock
                tree = Tree_Globalock.deserialize(cached_tree['tree'])
            else:
                # build tree with subtree locking
                tree = Tree_Sublock.deserialize(cached_tree['tree'])
            logs = [log]
            tree, last_ts = rebuild_tree(logs, tree)
        else:
            # get_logs
            logs = get_logs()
            tree, last_ts = rebuild_tree(logs, None)
    else:
        # get_logs
        logs = get_logs()
        tree, last_ts = rebuild_tree(logs, None)
    return tree, last_ts

def callback(ch, method, properties, body):
    message = json.loads(body)
    from_replica = message.get("from", "")
    msg = json.dumps(message.get("msg", ""))
    msg_ts = message.get("msg", "").get("ts","")
    logging = json.dumps({"ts":msg_ts, "time":str(datetime.now())})

    # got message
    log_file = os.path.join('/', 'usr', 'data', f'time{from_replica}.txt')
    with open(log_file, "a") as l:
        l.write(f"{logging}\n")

    # logging
    f_to_write = os.path.join('/', 'usr', 'data', f'{from_replica}.txt')
    with open(f_to_write, "a") as f:
        f.write(f"{msg}\n")

    # tree, last_ts = apply_log(message.get("msg", ""))
    # updating ts
    cache_client.set(from_replica+'-'+queue_to_cosume, msg_ts[replicas.index(from_replica)])
    # updating tree
    # cache_client.set(queue_to_cosume+'-tree', json.dumps({'ts':last_ts, 'tree':tree}))

    print(f"Read the message: {body}")

channel.basic_consume(
    queue=queue_to_cosume, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
