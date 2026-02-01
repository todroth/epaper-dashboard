import datetime

from astral import LocationInfo
from astral.sun import sun

from dashboard.provider.basedataprovider import BaseDataProvider
from dashboard.provider.sun.sundata import SunData


class SunProvider(BaseDataProvider):

    def load(self) -> SunData:
        location = LocationInfo(latitude=self.location_lat, longitude=self.location_lon)
        sun_info = sun(location.observer, date=datetime.date.today())
        sunrise_time = sun_info["sunrise"].strftime("%-H:%M")
        sunset_time = sun_info["sunset"].strftime("%-H:%M")
        return SunData(sunrise_time, sunset_time)