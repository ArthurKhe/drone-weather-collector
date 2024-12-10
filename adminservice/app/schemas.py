from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DronDataCreate(BaseModel):
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    latitude: float
    longitude: float
