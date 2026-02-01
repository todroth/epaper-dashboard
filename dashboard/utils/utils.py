import locale
import logging
import os

import requests


def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

def configure_locale():
    locale.setlocale(locale.LC_ALL, os.getenv("LOCALE", "en_US.UTF-8"))

def fetch_json(url: str, headers: dict = None):
    logging.info(f"Fetching {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()