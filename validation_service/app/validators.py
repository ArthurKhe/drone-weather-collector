from datetime import datetime
import logging
import requests
logging.basicConfig(level=logging.INFO)
TEMPERATURE_MIN = -50
TEMPERATURE_MAX = 50
HUMIDITY_MIN = 0
HUMIDITY_MAX = 100


def get_dron_from_admin_service(dron_id, token):
    try:
        url = f"http://adminservice:8001/dron/{dron_id}?token={token}"
        logging.info(f"send dron data URL: {url}")
        response = requests.get(
            url,
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
    if not (TEMPERATURE_MIN <= data["temperature"] <= TEMPERATURE_MAX):
        raise ValueError(f"Temperature out of range: {data['temperature']}")
    if not (HUMIDITY_MIN <= data["humidity"] <= HUMIDITY_MAX):
        raise ValueError(f"Humidity out of range: {data['humidity']}")

    if not (-90 <= data["latitude"] <= 90):
        raise ValueError(f"Latitude out of range: {data['latitude']}")
    if not (-180 <= data["longitude"] <= 180):
        raise ValueError(f"Longitude out of range: {data['longitude']}")
