import os


class Settings:
    ADMIN_SERVICE_URL = os.getenv("ADMIN_SERVICE_URL", "http://adminservice:8001")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "q1")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
    RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER", "rabbitmq")
    RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "rabbitmq")
    TEMPERATURE_MIN = int(os.getenv("TEMPERATURE_MIN", -50))
    TEMPERATURE_MAX = int(os.getenv("TEMPERATURE_MAX", 50))
    HUMIDITY_MIN = int(os.getenv("HUMIDITY_MIN", 0))
    HUMIDITY_MAX = int(os.getenv("HUMIDITY_MAX", 100))


settings = Settings()
