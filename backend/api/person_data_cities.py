import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

DIRECTUS_URL = os.getenv("DIRECTUS_URL")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")


# -------------------------
# NORMALIZATION
# -------------------------

def normalize_city(city: str):
    """
    Cleans historical / messy place strings
    """

    if not city:
        return None

    city = city.strip()

    # fix known country abbreviations / separators
    #city = city.replace("Frankr.", "France")
    #city = city.replace("Polen", "Poland")
    #city = city.replace("Hell.", "Netherlands")

    # remove suffixes like "/ Polen"
    city = city.split("/")[0]
    city = city.split("(")[0]

    # clean multiple spaces
    city = " ".join(city.split())

    # normalize unknowns
    if city.lower() in ["unknown", "n/a", "", "null"]:
        return "Unknown"

    return city


# -------------------------
# DATA EXTRACTION
# -------------------------

def get_city_dataset():
    """
    Returns:
    {
        city: {
            country: count
        }
    }
    """

    if not DIRECTUS_URL or not DIRECTUS_TOKEN:
        raise RuntimeError("Missing DIRECTUS_URL or DIRECTUS_TOKEN")

    url = f"{DIRECTUS_URL}/items/Person"

    params = {
        "fields": "PlaceOfBirth,Nationality",
        "limit": -1
    }

    headers = {
        "Authorization": f"Bearer {DIRECTUS_TOKEN}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("Error:", response.text)
        return {}

    data = response.json().get("data", [])

    city_country_counts = {}

    for item in data:
        city = normalize_city(item.get("PlaceOfBirth"))
        country = item.get("Nationality")

        if not city or not country:
            continue

        city = city.strip()
        country = country.strip()

        if city not in city_country_counts:
            city_country_counts[city] = {}

        city_country_counts[city][country] = (
            city_country_counts[city].get(country, 0) + 1
        )

    return city_country_counts


# -------------------------
# FLATTEN FOR GEOCODING
# -------------------------

def build_geocoding_tasks(city_country_counts):
    """
    Converts structure into:
    [(city, country, count), ...]
    """

    tasks = []

    for city, countries in city_country_counts.items():
        for country, count in countries.items():
            tasks.append((city, country, count))

    return tasks


# -------------------------
# OPTIONAL: CITY COUNTS ONLY
# -------------------------

def get_city_counts(city_country_counts):
    """
    Aggregates total counts per city
    """

    return {
        city: sum(countries.values())
        for city, countries in city_country_counts.items()
    }


# -------------------------
# TEST RUN
# -------------------------

if __name__ == "__main__":
    city_country_counts = get_city_dataset()

    print("\nRAW SPLIT DATA:")
    print(list(city_country_counts.items())[:5])

    city_counts = get_city_counts(city_country_counts)

    print("\nCITY TOTAL COUNTS:")
    print(list(city_counts.items())[:5])

    geocoding_tasks = build_geocoding_tasks(city_country_counts)

    print("\nGEOCODING TASKS SAMPLE:")
    print(geocoding_tasks[:10])