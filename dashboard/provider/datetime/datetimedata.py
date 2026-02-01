from dataclasses import dataclass

from datetime import datetime, date

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

@dataclass
class DateTimeData:
    datetime: str

    @classmethod
    def from_date(cls, datetime_obj: date):
        datetime_str = datetime.strftime(datetime_obj, DATETIME_FORMAT)
        return cls(datetime_str)

    def day_name(self) -> str:
        return datetime.strftime(self.to_date(), "%A")

    def date_str(self) -> str:
        return datetime.strftime(self.to_date(), "%d. %B %Y")

    def to_date(self):
        return datetime.strptime(self.datetime, DATETIME_FORMAT)

    def to_dict(self) -> dict:
        return {
            "DAY_NAME": self.day_name(),
            "DATE_STR": self.date_str(),
        }
