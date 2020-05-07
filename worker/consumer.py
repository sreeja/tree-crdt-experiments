import time
import os
import pika
import json
from datetime import datetime

latency_config = {
    "paris-bangalore": .144,
    "paris-newyork": .075,
    "bangalore-paris": .144,
    "bangalore-newyork": .215,
    "newyork-paris": .075,
    "newyork-bangalore": .215,
}

# latency_config = {
#     "paris-bangalore": 1,
#     "paris-newyork": .075,
#     "bangalore-paris": .144,
#     "bangalore-newyork": .215,
#     "newyork-paris": .075,
#     "newyork-bangalore": .215,
# }


time.sleep(30)  # A hack for rabbitmq to start
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='messenger'))
channel = connection.channel()

queue_to_cosume = os.environ.get("WHOAMI")
print(queue_to_cosume)
channel.queue_declare(queue=queue_to_cosume)

def callback(ch, method, properties, body):
    time.sleep(latency_config[queue_to_cosume])
    message = json.loads(body)
    from_replica = message.get("from", "")
    msg = json.dumps(message.get("msg", ""))
    msg_ts = message.get("msg", "").get("ts","")
    logging = json.dumps({"ts":msg_ts, "time":str(datetime.now())})
    log_file = os.path.join('/', 'usr', 'data', f'time{from_replica}.txt')
    with open(log_file, "a") as l:
        l.write(f"{logging}\n")
    f_to_write = os.path.join('/', 'usr', 'data', f'{from_replica}.txt')
    with open(f_to_write, "a") as f:
        f.write(f"{msg}\n")
    print(f"Read the message: {body}")

channel.basic_consume(
    queue=queue_to_cosume, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
