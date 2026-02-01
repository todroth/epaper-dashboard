import os
from abc import ABC


class BaseDataProvider(ABC):

    location_lat: float
    location_lon: float
    timezone: str

    def __init__(self):
        self.location_lat = os.getenv("LOCATION_LAT")
        self.location_lon = os.getenv("LOCATION_LON")
        self.timezone = os.getenv("TIMEZONE")
