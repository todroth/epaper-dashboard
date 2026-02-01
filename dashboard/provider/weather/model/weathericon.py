from enum import Enum, auto

from dashboard.utils.files import read_icon_path


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

    def to_svg(self) -> str:
        icon_filename = {
            WeatherIcon.CLEAR_DAY: "clear_day.svg",
            WeatherIcon.CLEAR_NIGHT: "clear_night.svg",
            WeatherIcon.PARTLY_CLOUDY_DAY: "partly_cloudy_day.svg",
            WeatherIcon.PARTLY_CLOUDY_NIGHT: "partly_cloudy_night.svg",
            WeatherIcon.CLOUDY: "cloudy.svg",
            WeatherIcon.FOG: "fog.svg",
            WeatherIcon.WIND: "wind.svg",
            WeatherIcon.RAIN: "rain.svg",
            WeatherIcon.SLEET: "sleet.svg",
            WeatherIcon.SNOW: "snow.svg",
            WeatherIcon.HAIL: "hail.svg",
            WeatherIcon.THUNDERSTORM: "thunderstorm.svg",
            WeatherIcon.NONE: "none.svg"
        }.get(self)

        return read_icon_path(icon_filename)

    def to_str(self) -> str:
        return {
            WeatherIcon.CLEAR_DAY: "Sonne",
            WeatherIcon.CLEAR_NIGHT: "Klare Nacht",
            WeatherIcon.PARTLY_CLOUDY_DAY: "Leicht Bewölkt",
            WeatherIcon.PARTLY_CLOUDY_NIGHT: "Leicht bewölkte Nacht",
            WeatherIcon.CLOUDY: "Wolken",
            WeatherIcon.FOG: "Nebel",
            WeatherIcon.WIND: "Wind",
            WeatherIcon.RAIN: "Regen",
            WeatherIcon.SLEET: "Schneeregen",
            WeatherIcon.SNOW: "Schnee",
            WeatherIcon.HAIL: "Hagel",
            WeatherIcon.THUNDERSTORM: "Gewitter",
            WeatherIcon.NONE: "Unbekannt"
        }.get(self)
