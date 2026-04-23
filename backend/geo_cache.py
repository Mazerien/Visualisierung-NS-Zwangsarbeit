import requests
import json
import os

OHM_URL = "http://localhost:5000/api/ohm"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "city_cache.json")

os.makedirs(CACHE_DIR, exist_ok=True)

# Load cache from file if it exists
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r") as f:
            _CACHE = json.load(f)
    except json.JSONDecodeError:
        _CACHE = {}
else:
    _CACHE = {}


def _make_key(city_name: str, country: str, year: int) -> str:
    """Create a JSON-safe cache key."""
    return f"{city_name.lower()}|{country.lower() if country else ''}|{year}"


def _save_cache():
    """Persist cache to disk."""
    with open(CACHE_FILE, "w") as f:
        json.dump(_CACHE, f)


def get_city_coords(city_name: str, country: str = None, year: int = 1938):
    """Cached access to OHM API with persistent storage."""

    key = _make_key(city_name, country, year)

    # Return from cache if available
    if key in _CACHE:
        return _CACHE[key]

    # Call API only if not cached
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

    # Store result (even None to avoid repeated failed calls)
    _CACHE[key] = coords
    _save_cache()

    return coords


def preload_cities(cities: list[tuple]):
    """
    Preload coordinates at app startup.
    cities = [(city, country), ...]
    """
    for city, country in cities:
        get_city_coords(city, country)

    _save_cache()