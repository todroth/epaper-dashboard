import logging

import requests


def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

def fetch_json(url: str, headers: dict = None):
    logging.info(f"Fetching {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()