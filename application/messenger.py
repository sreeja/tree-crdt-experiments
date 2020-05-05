import os
import json
import time
from contextlib import contextmanager

import pika


latency_config = {
    "paris": {
        "bangalore": .144,
        "newyork": .075
    },
    "bangalore": {
        "paris": .144,
        "newyork": .215,
    },
    "newyork": {
        "paris": .075,
        "bangalore": .215,
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
    payload = json.dumps(
        {
            "msg": message.get("msg", ""),
            "from": os.environ.get("WHOAMI")
        })
    queue_name = message.get("to", "")

    time.sleep(config.get(queue_name, 0))
    with messenger_channel() as channel:
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=payload)
    print(f"wrote to {queue_name}", flush=True)
