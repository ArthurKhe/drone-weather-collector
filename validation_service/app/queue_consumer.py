import json
import requests
import logging
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from settings import settings


logging.basicConfig(level=logging.INFO)

credentials = PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)


def send_data_to_admin_service(data):
    try:
        url = f"{settings.ADMIN_SERVICE_URL}/dron/{data['dron_id']}/data"
        logging.info(f"send dron data URL: {url}")
        response = requests.post(
            url,
            json=data,
            headers={
                "token": data.get("token")
            }
        )
        response.raise_for_status()
        logging.info(f"Data successfully sent to admin service: {response.json()}")
    except requests.RequestException as e:
        logging.info(f"Failed to send data to admin service: {e}")


def consume_messages():
    logging.info("Start consumer")
    connection = BlockingConnection(ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=5672,
        credentials=credentials,
    ))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        logging.info(f"Received message: {body}")
        try:
            message = json.loads(body)
            send_data_to_admin_service(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.info(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(settings.RABBITMQ_QUEUE, on_message_callback=callback)
    logging.info("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
