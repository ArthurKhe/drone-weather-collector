import os
import json
import requests
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
import logging

logging.basicConfig(level=logging.INFO)
ADMIN_SERVICE_URL = os.getenv("ADMIN_SERVICE_URL", "http://adminservice:8001")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "q1")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER", "rabbitmq")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "rabbitmq")
credentials = PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)


def send_data_to_admin_service(data):
    try:
        url = f"{ADMIN_SERVICE_URL}/dron/{data['dron_id']}/data"
        logging.info(f"send dron data URL: {url}")
        response = requests.post(
            f"{ADMIN_SERVICE_URL}/dron/{data['dron_id']}/data",
            json=data,
        )
        response.raise_for_status()
        logging.info(f"Data successfully sent to admin service: {response.json()}")
    except requests.RequestException as e:
        logging.info(f"Failed to send data to admin service: {e}")


def consume_messages():
    logging.info("Start consumer")
    connection = BlockingConnection(ConnectionParameters(
        host=RABBITMQ_HOST,
        port=5672,
        credentials=credentials,
    ))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        logging.info(f"Received message: {body}")
        try:
            message = json.loads(body)
            send_data_to_admin_service(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.info(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue=os.getenv("RABBITMQ_QUEUE", "q1"), on_message_callback=callback)
    logging.info("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
