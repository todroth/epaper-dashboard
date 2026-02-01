from datetime import datetime

from dashboard.provider.basedataprovider import BaseDataProvider
from dashboard.provider.datetime.datetimedata import DateTimeData


class DateTimeProvider(BaseDataProvider):

    def load(self) -> DateTimeData:
        datetime_data = datetime.now()
        return DateTimeData.from_date(datetime_data)