import time
import os
import pika


time.sleep(60)  # A hack for rabbitmq to start
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='messenger'))
channel = connection.channel()

queue_to_cosume = os.environ.get("WHOAMI")
channel.queue_declare(queue=queue_to_cosume)


def callback(ch, method, properties, body):
    print("Read the message", flush=True)
    # with open("/usr/data/myfile", "w") as f:
    #     f.write("Created")

channel.basic_consume(
    queue=queue_to_cosume, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
