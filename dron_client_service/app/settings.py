import os
from dotenv import load_dotenv

load_dotenv("config.env")


class Settings:
    GRPC_SERVER_ADDRESS = os.getenv("GRPC_SERVER_ADDRESS", "0.0.0.0:50051")
    AUTH_SERVER_URL = os.getenv("AUTH_SERVER_URL", "http://127.0.0.1:8000")
    DRON_ID = int(os.getenv("DRON_ID"))
    DRON_NAME = os.getenv("DRON_NAME")
    DRON_PASS = os.getenv("DRON_PASS")
    PERIOD_SEND_DATA = int(os.getenv("PERIOD_SEND_DATA", "10"))


settings = Settings()
