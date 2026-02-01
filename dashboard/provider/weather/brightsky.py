from datetime import datetime

from dashboard.provider.weather.baseweatherprovider import BaseWeatherProvider
from dashboard.utils.utils import fetch_json
from dashboard.provider.weather.model.weatherdata import WeatherData
from dashboard.provider.weather.model.weathericon import WeatherIcon


class Brightsky(BaseWeatherProvider):

    BASE_URL = "https://api.brightsky.dev/weather?lat={}&lon={}&date={}&tz={}"

    ICON_MAPPING = {
        "clear-day": WeatherIcon.CLEAR_DAY,
        "clear-night": WeatherIcon.CLEAR_NIGHT,
        "partly-cloudy-day": WeatherIcon.PARTLY_CLOUDY_DAY,
        "partly-cloudy-night": WeatherIcon.PARTLY_CLOUDY_NIGHT,
        "cloudy": WeatherIcon.CLOUDY,
        "fog": WeatherIcon.FOG,
        "wind": WeatherIcon.WIND,
        "rain": WeatherIcon.RAIN,
        "sleet": WeatherIcon.SLEET,
        "snow": WeatherIcon.SNOW,
        "hail": WeatherIcon.HAIL,
        "thunderstorm": WeatherIcon.THUNDERSTORM
    }

    def __init__(self):
        super().__init__()

    def load(self) -> WeatherData:
        url = self.get_url()
        json = fetch_json(url)
        return Brightsky.to_weather_data(json)

    def get_url(self) -> str:
        today = datetime.now().strftime("%Y-%m-%d")
        url = self.BASE_URL.format(self.location_lat, self.location_lon, today, self.timezone)
        return url

    @staticmethod
    def to_weather_data(json) -> WeatherData:

        weather_day = json.get("weather", None)
        if not weather_day:
            raise ValueError("No weather data")

        temperatures = [weather_hour["temperature"] for weather_hour in weather_day]
        temp_min = min(temperatures)
        temp_max = max(temperatures)

        icon = Brightsky.get_icon(weather_day)

        return WeatherData(temp_min=temp_min, temp_max=temp_max, icon=icon)

    @staticmethod
    def get_icon(weather_day) -> WeatherIcon:

        weather_noon = next(
            (weather for weather in weather_day if datetime.fromisoformat(weather["timestamp"]).hour == 12),
            None
        )

        icon_str = weather_noon.get("icon", None) if weather_noon else None

        return Brightsky.ICON_MAPPING.get(icon_str, WeatherIcon.NONE)
