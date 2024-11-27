import requests
from fastapi import HTTPException, status

AUTH_SERVICE_URL = "http://authservice:8000"


def validate_token(token: str):
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/me", headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
