import os

from dotenv import load_dotenv

from dashboard.provider.weather.brightskyweatherprovider import BrightskyWeatherProvider
from dashboard.provider.weather.weatherdata import WeatherData
from dashboard.utils.files import write_json
from dashboard.utils.utils import configure_logging, configure_locale

DATA_FILE_NAME = "weather.json"

def main():
    load_dotenv()
    configure_logging()
    configure_locale()
    weather_data = load_weather()
    write_json(weather_data, DATA_FILE_NAME)
    print(weather_data)

def load_weather() -> WeatherData:

    weather_provider_name = os.getenv("WEATHER_PROVIDER")
    weather_provider = None

    match weather_provider_name:
        case "brightsky":
            weather_provider = BrightskyWeatherProvider()
        case _: raise Exception(f"Weather provider {weather_provider_name} not supported")

    weather_data = weather_provider.load()
    if weather_data is None:
        raise Exception(f"No weather data found for provider {weather_provider_name}")

    return weather_provider.load()

if __name__ == "__main__":
    main()
