from dotenv import load_dotenv

from dashboard.provider.datetime.datetimeprovider import DateTimeProvider
from dashboard.provider.datetime.datetimedata import DateTimeData
from dashboard.utils.files import write_json
from dashboard.utils.utils import configure_logging, configure_locale

DATA_FILE_NAME = "datetime.json"

def main():
    load_dotenv()
    configure_logging()
    configure_locale()
    datetime_data = load_datetime()
    write_json(datetime_data, DATA_FILE_NAME)
    print(datetime_data)

def load_datetime() -> DateTimeData:
    return DateTimeProvider().load()

if __name__ == "__main__":
    main()
