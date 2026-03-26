# geo_cache.py

import requests

_CACHE = {}

OHM_URL = "http://localhost:5000/ohm"


def get_city_coords(city_name: str, country: str = None, year: int = 1938):
    """Cached access to OHM API."""

    key = (city_name.lower(), country.lower() if country else None, year)

    if key in _CACHE:
        return _CACHE[key]

    # Call API only once
    params = {"name": city_name, "year": year}
    if country:
        params["country"] = country

    response = requests.get(OHM_URL, params=params)
    data = response.json()

    coords = None

    if isinstance(data, list) and len(data) > 0:
        for item in data:
            c = item.get("coordinates")
            if not c:
                continue

            if country:
                country_str = str(item.get("country", "")).lower()
                if country.lower() not in country_str and country_str not in country.lower():
                    continue

            coords = [c["lat"], c["lon"]]
            break

    _CACHE[key] = coords
    return coords


def preload_cities(cities: list[tuple]):
    """
    Preload coordinates at app startup.
    cities = [(city, country), ...]
    """
    for city, country in cities:
        get_city_coords(city, country)