import os
import time
from contextlib import contextmanager

import pika


latency_config = {
    "paris": {
        "bangalore": 2,
        "newyork": 1
    },
    "bangalore": {
        "paris": 2,
        "newyork": 3,
    },
    "newyork": {
        "paris": 1,
        "bangalore": 3,
    }
}

@contextmanager
def messenger_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('messenger'))
    channel = connection.channel()
    yield channel
    connection.close()

def get_config():
    whoami = os.environ.get("WHOAMI")
    return latency_config.get(whoami, {})

def write_message(message):
    config = get_config()
    payload = message.get("payload", "")
    queue_name = message.get("to", "")

    print(f"writing to {queue_name}", flush=True)

    time.sleep(config.get(queue_name, 0))
    # write to the queue

    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='messenger'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(f"Sent Hello World to {queue_name}", flush=True)
    connection.close()

    # with messenger_channel() as channel:
    #     channel.queue_declare(queue=queue_name)
    #     channel.basic_publish(exchange='',
    #                           routing_key='hello',
    #                           body=payload)
