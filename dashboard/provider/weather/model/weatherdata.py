from dataclasses import dataclass

from dashboard.provider.weather.model.weathericon import WeatherIcon

@dataclass
class WeatherData:
    temp_min: int
    temp_max: int
    icon: WeatherIcon
