from dataclasses import dataclass


@dataclass
class SunData:
    sunrise_time: str
    sunset_time: str

    def to_dict(self) -> dict:
        return {
            "SUNRISE_TIME": self.sunrise_time,
            "SUNSET_TIME": self.sunset_time
        }