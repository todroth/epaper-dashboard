from dashboard.provider.alert.basealertprovider import BaseAlertProvider
from dashboard.provider.alert.model.alertdata import AlertData
from dashboard.utils.utils import fetch_json


class Brightsky(BaseAlertProvider):

    BASE_URL = "https://api.brightsky.dev/alerts?lat={}&lon={}&tz={}"

    def __init__(self):
        super().__init__()

    def load(self) -> AlertData:
        url = self.get_url()
        json = fetch_json(url)
        return Brightsky.to_alert_data(json)

    def get_url(self):
        url = self.BASE_URL.format(self.location_lat, self.location_lon, self.timezone)
        return url

    @staticmethod
    def to_alert_data(json) -> AlertData:
        alerts = json.get("alerts", [])

        severe_alerts = [
            alert for alert in alerts
            if alert.get("severity") in ["severe", "extreme"]
        ]

        if not severe_alerts:
            return AlertData.empty()

        severity_order = {"extreme": 0, "severe": 1}
        most_severe = min(severe_alerts, key=lambda a: severity_order.get(a.get("severity"), 99))

        return AlertData(
            headline=most_severe.get("headline_de", ""),
            description=most_severe.get("description_de", ""),
            instruction=most_severe.get("instruction_de", "")
        )

