import time
import os
import pika
import json
from datetime import datetime
from pymemcache.client.base import Client

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

def apply_log(log):
    # cache_client.get(queue_to_cosume+'-tree', )
    if exp == 0:
        # build CRDT tree
        pass
    elif exp == 1:
        # build opsets tree
        pass
    elif exp == 2:
        # build tree with single lock
        pass
    else:
        # build tree with subtree locking
        pass


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
    # updating ts
    cache_client.set(from_replica+'-'+queue_to_cosume, msg_ts[replicas.index(from_replica)])

    apply_log(msg)
    print(f"Read the message: {body}")

channel.basic_consume(
    queue=queue_to_cosume, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
