"""
TODO: Docstring
"""
import os
import requests
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
    # city = city.replace("Frankr.", "France")
    # city = city.replace("Polen", "Poland")
    # city = city.replace("Hell.", "Netherlands")

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
            countries: { country: count },
            people: [{first_name, last_name}]
        }
    }
    """

    if not DIRECTUS_URL or not DIRECTUS_TOKEN:
        raise RuntimeError("Missing DIRECTUS_URL or DIRECTUS_TOKEN")

    url = f"{DIRECTUS_URL}/items/Person"

    params = {
        "fields": "PlaceOfBirth,Nationality,FirstName,LastName",
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

    city_data = {}

    for item in data:
        city = normalize_city(item.get("PlaceOfBirth"))
        country = item.get("Nationality")

        first = item.get("FirstName")
        last = item.get("LastName")

        if not city or not country:
            continue

        city = city.strip()
        country = country.strip()

        if city not in city_data:
            city_data[city] = {
                "countries": {},
                "people": []
            }

        city_data[city]["countries"][country] = (
            city_data[city]["countries"].get(country, 0) + 1
        )

        if first or last:
            city_data[city]["people"].append({
                "first_name": first,
                "last_name": last
            })

    return city_data


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
    Safely aggregates counts per city even if structure contains nested dicts.
    """

    result = {}

    for city, countries in city_country_counts.items():

        total = 0

        for value in countries.values():

            if isinstance(value, (int, float)):
                total += value

            elif isinstance(value, dict):
                total += sum(
                    v for v in value.values()
                    if isinstance(v, (int, float))
                )

        result[city] = total

    return result


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
