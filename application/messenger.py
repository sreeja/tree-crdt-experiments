import os
import json
import time
from contextlib import contextmanager

import pika
from flask import current_app

# @contextmanager
# def messenger_connection():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('messenger'))
#     yield connection
#     connection.close()

# def get_config():
#     whoami = os.environ.get("WHOAMI")
#     return latency_config.get(whoami, {})

def write_message(message):
    latency_config = current_app.config["latency_config"]
    whoami = os.environ.get("WHOAMI")
    payload = json.dumps(
        {
            "msg": message.get("msg", ""),
            "from": whoami
        })
    queue_name = message.get("to", "")

    channel_name = whoami + '-' + queue_name

    connection = pika.BlockingConnection(pika.ConnectionParameters('messenger'))
    channel = connection.channel()
    channel.confirm_delivery() 

    # time.sleep(config.get(queue_name, 0))
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange='amq.direct',
                    queue=queue_name)
        # channel.basic_publish(exchange='',
        #                     routing_key=queue_name,
        #                     body=payload)

    # Create our delay channel.
    delay_channel = connection.channel()
    delay_channel.confirm_delivery()

    # This is where we declare the delay, and routing for our delay channel.
    # print(latency_config[queue_name]*1000*100)
    delay_channel.queue_declare(queue=channel_name+'_delay', durable=True,  arguments={
    'x-message-ttl' : int(latency_config[channel_name]*1000), # Delay until the message is transferred in milliseconds.
    'x-dead-letter-exchange' : 'amq.direct', # Exchange used to transfer the message from A to B.
    'x-dead-letter-routing-key' : queue_name # Name of the queue we want the message transferred to.
    })

    delay_channel.basic_publish(exchange='',
                        routing_key=channel_name+'_delay',
                        body=payload,
                        properties=pika.BasicProperties(delivery_mode=2))

    connection.close()
    # print(f"wrote to {queue_name}", flush=True)
