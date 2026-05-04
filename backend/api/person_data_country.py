"""
TODO: Docstring
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DIRECTUS_URL = os.getenv("DIRECTUS_URL")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")


COUNTRY_MAP = {
        "Germany": "Berlin",
        "France": "Paris",
        "Belgium": "Antwerpen",
        "Croatia": "Zagreb",
        "Czechia": "Ostrau",
        "Poland": "Krakau",
        "Soviet Union": "Москва",
        "Spain": "Barcelona",
        "The Netherlands": "Rotterdam",
        "Ukraine": "Kiew",
        "United Kingdom": "Gillingham",
        "Unknown": "Unknown"
    }


def get_nationality_counts():
    """TODO: Docstring"""
    load_dotenv("../.env")
    directus_url = os.getenv("DIRECTUS_URL")
    directus_token = os.getenv("DIRECTUS_TOKEN")

    if not directus_url or not directus_token:
        raise RuntimeError("Missing DIRECTUS_URL or DIRECTUS_TOKEN")

    url = f"{DIRECTUS_URL}/items/Person"

    params = {
        "aggregate[count]": "*",
        "groupBy": "Nationality"
    }

    headers = {
        "Authorization": f"Bearer {DIRECTUS_TOKEN}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("Error:", response.text)
        return {}

    data = response.json().get("data", [])

    raw_counts = {
        item["Nationality"]: item["count"]
        for item in data
    }

    normalized = {}

    for api_country, count in raw_counts.items():
        mapped = COUNTRY_MAP.get(api_country, api_country)

        normalized[mapped] = normalized.get(mapped, 0) + count

    return normalized
