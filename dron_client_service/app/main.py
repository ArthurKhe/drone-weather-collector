import grpc
import os
from proto import dron_pb2_grpc
from proto import dron_pb2
import logging
import requests
import random
from time import sleep
from datetime import datetime
logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv

load_dotenv("config.env")
GRPC_SERVER_ADDRESS = os.getenv("GRPC_SERVER_ADDRESS", "0.0.0.0:50051")
DRON_ID = int(os.getenv("DRON_ID"))
DRON_NAME = os.getenv("DRON_NAME")
DRON_PASS = os.getenv("DRON_PASS")
PERIOD_SEND_DATA = int(os.getenv("PERIOD_SEND_DATA", "10"))


def get_random_number():
    return random.randint(-100, 100)


def get_acceess_token():
    try:
        url = f"http://127.0.0.1:8000/login"
        logging.info(f"send request URL: {url}")
        response = requests.post(
            url,
            data={
                "username": DRON_NAME,
                "password": DRON_PASS,
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
    with grpc.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = dron_pb2_grpc.DronValidationStub(channel)
        print(f"Connecting to gRPC server at {GRPC_SERVER_ADDRESS}")
        token = get_acceess_token()
        # Пример данных
        while True:

            request = dron_pb2.ValidationRequest(
                dron_id=DRON_ID,
                temperature=get_random_number(),
                humidity=get_random_number(),
                timestamp=datetime.now().isoformat(),
                latitude=59.934280,
                longitude=30.335099,
                token=token,
            )
            try:
                response = stub.ValidateData(request)
                if response.is_valid:
                    logging.info("Validation succeeded!")
                else:
                    logging.info(f"Validation failed: {response.message}")
            except grpc.RpcError as e:
                logging.info(f"gRPC call failed: {e.details()}")
            sleep(PERIOD_SEND_DATA)


if __name__ == "__main__":
    run_client()
