import os
import json
import time
from contextlib import contextmanager

import pika


@contextmanager
def messenger_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('messenger'))
    channel = connection.channel()
    yield channel
    connection.close()

# def get_config():
#     whoami = os.environ.get("WHOAMI")
#     return latency_config.get(whoami, {})

def write_message(message):
    whoami = os.environ.get("WHOAMI")
    payload = json.dumps(
        {
            "msg": message.get("msg", ""),
            "from": whoami
        })
    queue_name = whoami + "-" + message.get("to", "")

    # time.sleep(config.get(queue_name, 0))
    with messenger_channel() as channel:
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=payload)
    print(f"wrote to {queue_name}", flush=True)
