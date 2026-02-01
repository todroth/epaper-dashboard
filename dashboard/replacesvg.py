import json

from dotenv import load_dotenv

import dashboard.getweather
from dashboard.provider.weather.model.weatherdata import WeatherData
from dashboard.utils.files import read_json, read_template, write_template
from dashboard.utils.utils import configure_logging


def main():
    load_dotenv()
    configure_logging()

    values = read_json(dashboard.getweather.DATA_FILE_NAME, WeatherData).to_dict()

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
