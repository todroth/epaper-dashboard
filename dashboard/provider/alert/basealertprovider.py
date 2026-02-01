from abc import abstractmethod

from dashboard.provider.alert.alertdata import AlertData
from dashboard.provider.basedataprovider import BaseDataProvider


class BaseAlertProvider(BaseDataProvider):

    @abstractmethod
    def load(self) -> AlertData:
        pass