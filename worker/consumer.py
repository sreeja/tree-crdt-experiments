import time
import os
import pika


time.sleep(60)  # A hack for rabbitmq to start
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='messenger'))
channel = connection.channel()

queue_to_cosume = os.environ.get("WHOAMI")
print(queue_to_cosume)
channel.queue_declare(queue=queue_to_cosume)


def callback(ch, method, properties, body):
    print(f"Read the message: {body}")

channel.basic_consume(
    queue=queue_to_cosume, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
