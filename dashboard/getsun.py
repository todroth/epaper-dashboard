from dotenv import load_dotenv

from dashboard.provider.sun.model.sundata import SunData
from dashboard.provider.sun.sunprovider import SunProvider
from dashboard.utils.files import write_json
from dashboard.utils.utils import configure_logging, configure_locale

DATA_FILE_NAME = "sun.json"

def main():
    load_dotenv()
    configure_logging()
    configure_locale()
    sun_data = load_sun()
    write_json(sun_data, DATA_FILE_NAME)
    print(sun_data)

def load_sun() -> SunData:
    return SunProvider().load()

if __name__ == "__main__":
    main()
