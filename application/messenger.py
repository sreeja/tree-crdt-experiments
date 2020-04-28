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

def write(message):
    to = message.get("to", "")
    payload = message.get("payload", "")
    queue_name = f"{whoami}-{to}"
    time.sleep(config.get(to, 0))
    # write to the queue
    with messenger_channel() as chn:
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=payload)
