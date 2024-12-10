import os
import pika
import logging

logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "q1")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672),
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER", "rabbitmq")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "rabbitmq")
credentials = pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)


def publish_to_queue(message):
    logging.info(f"connect to RABBIT")
    logging.info(f"[MESSAGE]: {message}")

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=5672,
        credentials=credentials,
    ))
    channel = connection.channel()
    logging.info(f"SUCCESS connect to RABBIT")
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=RABBITMQ_QUEUE,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    logging.info(f"Message published to queue: {message}")
    connection.close()
