import json

from dotenv import load_dotenv

from dashboard import getalert, getweather, getdatetime, getsun
from dashboard.provider.alert.model.alertdata import AlertData
from dashboard.provider.datetime.model.datetimedata import DateTimeData
from dashboard.provider.sun.model.sundata import SunData
from dashboard.provider.weather.model.weatherdata import WeatherData
from dashboard.utils.files import read_json, read_template, write_template
from dashboard.utils.utils import configure_logging, configure_locale


def main():
    load_dotenv()
    configure_logging()
    configure_locale()

    values = (
            read_json(getweather.DATA_FILE_NAME, WeatherData).to_dict()
            | read_json(getalert.DATA_FILE_NAME, AlertData).to_dict()
            | read_json(getdatetime.DATA_FILE_NAME, DateTimeData).to_dict()
            | read_json(getsun.DATA_FILE_NAME, SunData).to_dict()
    )

    template = read_template()
    updated_template = replace_placeholder(template, values)
    write_template(updated_template)

    print(json.dumps(values, indent=2))


def replace_placeholder(template: str, values: dict) -> str:
    for placeholder, replacement in values.items():
        template = template.replace(placeholder, replacement)
    return template


if __name__ == "__main__":
    main()
