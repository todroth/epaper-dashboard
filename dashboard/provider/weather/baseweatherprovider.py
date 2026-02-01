from abc import abstractmethod

from dashboard.provider.basedataprovider import BaseDataProvider
from dashboard.provider.weather.weatherdata import WeatherData


class BaseWeatherProvider(BaseDataProvider):

    @abstractmethod
    def load(self) -> WeatherData:
        pass
