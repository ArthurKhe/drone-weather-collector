import os
import pika
import logging
from settings import settings

logging.basicConfig(level=logging.INFO)

credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)


def publish_to_queue(message):
    logging.info(f"connect to RABBIT")
    logging.info(f"[MESSAGE]: {message}")

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=5672,
        credentials=credentials,
    ))
    channel = connection.channel()
    logging.info(f"SUCCESS connect to RABBIT")
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=settings.RABBITMQ_QUEUE,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    logging.info(f"Message published to queue: {message}")
    connection.close()
