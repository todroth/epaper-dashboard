from dataclasses import dataclass

from dashboard.provider.weather.model.weathericon import WeatherIcon

@dataclass
class WeatherData:
    temp_min: int
    temp_max: int
    icon: WeatherIcon

    def to_dict(self) -> dict[str, str]:
        return {
            "TEMP_MIN": str(self.temp_min),
            "TEMP_MAX": str(self.temp_max),
            "WEATHER_ICON": self.icon.to_svg(),
            "WEATHER_DESCRIPTION": self.icon.to_str()
        }
