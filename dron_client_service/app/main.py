import grpc
import os
from proto import dron_pb2_grpc
from proto import dron_pb2
import logging
import requests
import random
from time import sleep
from settings import settings
from datetime import datetime
logging.basicConfig(level=logging.INFO)



def get_random_number():
    return random.randint(-100, 100)


def get_acceess_token():
    try:
        url = f"{settings.AUTH_SERVER_URL}/login"
        logging.info(f"send request URL: {url}")
        response = requests.post(
            url,
            data={
                "username": settings.DRON_NAME,
                "password": settings.DRON_PASS,
            }
        )
        auth_data = response.json()
        response.raise_for_status()
        logging.info(f"Data successfully auth: {auth_data}")
        return auth_data.get("access_token")
    except requests.RequestException as e:
        logging.info(f"Failed get token: {e}")
        return None


def run_client():
    with grpc.insecure_channel(settings.GRPC_SERVER_ADDRESS) as channel:
        stub = dron_pb2_grpc.DronValidationStub(channel)
        print(f"Connecting to gRPC server at {settings.GRPC_SERVER_ADDRESS}")
        token = get_acceess_token()
        # Пример данных
        while True:

            request = dron_pb2.ValidationRequest(
                dron_id=settings.DRON_ID,
                temperature=get_random_number(),
                humidity=get_random_number(),
                timestamp=datetime.now().isoformat(),
                latitude=59.934280,
                longitude=30.335099,
                token=token,
            )
            try:
                logging.info(F"Dron {settings.DRON_NAME} send weather data\n{request}")
                response = stub.ValidateData(request)
                if response.is_valid:
                    logging.info("Validation succeeded!")
                else:
                    logging.info(f"Validation failed: {response.message}")
            except grpc.RpcError as e:
                logging.info(f"gRPC call failed: {e.details()}")
            sleep(settings.PERIOD_SEND_DATA)


if __name__ == "__main__":
    run_client()
