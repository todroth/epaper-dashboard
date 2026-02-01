import os

from dotenv import load_dotenv

from dashboard.provider.alert.brightskyalertprovider import BrightskyAlertProvider
from dashboard.provider.alert.alertdata import AlertData
from dashboard.utils.files import write_json
from dashboard.utils.utils import configure_logging, configure_locale

DATA_FILE_NAME = "alert.json"

def main():
    load_dotenv()
    configure_logging()
    configure_locale()
    alert_data = load_alert()
    write_json(alert_data, DATA_FILE_NAME)
    print(alert_data)

def load_alert() -> AlertData:

    alert_provider_name = os.getenv("ALERT_PROVIDER")
    alert_provider = None

    match alert_provider_name:
        case "brightsky":
            alert_provider = BrightskyAlertProvider()
        case _: raise Exception(f"Alert provider {alert_provider_name} not supported")

    alert_data = alert_provider.load()
    if alert_data is None:
        raise Exception(f"No alert data found for provider {alert_provider_name}")

    return alert_data

if __name__ == "__main__":
    main()
