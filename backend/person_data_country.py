"""
TODO: Docstring
"""
import os
import requests

TIMEOUT = 10


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

def get_directus_config():
    url = os.getenv("DIRECTUS_URL")
    token = os.getenv("DIRECTUS_TOKEN")

    if not url or not token:
        raise RuntimeError("Missing Directus env vars")

    return url, token


def get_nationality_counts():
    """TODO: Docstring"""
    directus_url, directus_token = get_directus_config()

    if not directus_url or not directus_token:
        raise RuntimeError("Missing directus_url or directus_token")

    url = f"{directus_url}/items/person_update"

    params = {
        "aggregate[count]": "*",
        "groupBy": "nationality"
    }

    headers = {
        "Authorization": f"Bearer {directus_token}"
    }

    response = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)

    if response.status_code != 200:
        print("Error:", response.text)
        return {}

    data = response.json().get("data", [])

    raw_counts = {
        item["nationality"]: item["count"]
        for item in data
    }

    normalized = {}

    for api_country, count in raw_counts.items():
        mapped = COUNTRY_MAP.get(api_country, api_country)

        normalized[mapped] = normalized.get(mapped, 0) + count

    return normalized
