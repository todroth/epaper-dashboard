from enum import Enum, auto


class WeatherIcon(Enum):
    CLEAR_DAY = auto()
    CLEAR_NIGHT = auto()
    PARTLY_CLOUDY_DAY = auto()
    PARTLY_CLOUDY_NIGHT = auto()
    CLOUDY = auto()
    FOG = auto()
    WIND = auto()
    RAIN = auto()
    SLEET = auto()
    SNOW = auto()
    HAIL = auto()
    THUNDERSTORM = auto()
    NONE = auto()