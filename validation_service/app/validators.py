
import logging
import requests
from datetime import datetime
from settings import settings
logging.basicConfig(level=logging.INFO)



def get_dron_from_admin_service(dron_id, token):
    try:
        url = f"{settings.ADMIN_SERVICE_URL}/dron/{dron_id}"
        logging.info(f"send dron data URL: {url}")
        response = requests.get(
            url,
            headers={
                "token": token
            }
        )
        dron_data = response.json()
        response.raise_for_status()
        logging.info(f"Data successfully GET from admin service: {dron_data}")
        return dron_data
    except requests.RequestException as e:
        logging.info(f"Failed to get data from admin service: {e}")
        return None


def validate_dron_data(data):
    required_fields = ["dron_id", "timestamp", "temperature", "humidity", "latitude", "longitude"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    try:
        datetime.fromisoformat(data["timestamp"])
    except ValueError:
        raise ValueError("Invalid timestamp format. Use ISO 8601.")
    dron = get_dron_from_admin_service(data['dron_id'], data['token'])
    if not dron:
        raise ValueError(f"Dron with id {data['dron_id']} not found")
    if not (settings.TEMPERATURE_MIN <= data["temperature"] <= settings.TEMPERATURE_MAX):
        raise ValueError(f"Temperature out of range: {data['temperature']}")
    if not (settings.HUMIDITY_MIN <= data["humidity"] <= settings.HUMIDITY_MAX):
        raise ValueError(f"Humidity out of range: {data['humidity']}")
