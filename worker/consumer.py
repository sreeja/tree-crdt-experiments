import time
import os
import pika
import json
from datetime import datetime, timedelta
import sched

# latency_config = {
#     "paris-bangalore": .144,
#     "paris-newyork": .075,
#     "bangalore-paris": .144,
#     "bangalore-newyork": .215,
#     "newyork-paris": .075,
#     "newyork-bangalore": .215,
# }

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
channel.queue_declare(queue=queue_to_cosume, durable=True)

time_log = {}
op_log = {}
from_log={}

# def flush():
#     print("calling flush")
#     print(time_log, datetime.now())
#     for each in time_log:
#         if each <= datetime.now():
#             entry = json.loads(time_log[each])
#             time_stamp = str(entry["ts"])
#             log_file = os.path.join('/', 'usr', 'data', f'time{from_log[time_stamp]}.txt')
#             with open(log_file, "a") as l:
#                 l.write(f"{time_log[each]}\n")
#             f_to_write = os.path.join('/', 'usr', 'data', f'{from_log[time_stamp]}.txt')
#             with open(f_to_write, "a") as f:
#                 f.write(f"{op_log[time_stamp]}\n")
#             print(f"Read the message: {op_log[time_stamp]}")



def callback(ch, method, properties, body):
    # time.sleep(latency_config[queue_to_cosume])
    # print(f"Got the message: {body}")
    # flush()
    #print("111111111", body)
    message = json.loads(body)
    from_replica = message.get("from", "")
    msg = json.dumps(message.get("msg", ""))
    msg_ts = message.get("msg", "").get("ts","")
    rec_time = datetime.now() + timedelta(seconds=latency_config[queue_to_cosume])
    logging = json.dumps({"ts":msg_ts, "time":str(rec_time)})

    # time_log[rec_time] = logging
    # op_log[str(msg_ts)] = msg
    # from_log[str(msg_ts)] = from_replica

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
