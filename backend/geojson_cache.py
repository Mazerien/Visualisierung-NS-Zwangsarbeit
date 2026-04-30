import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "geojson_cache.json")

os.makedirs(CACHE_DIR, exist_ok=True)

# Load cache
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r") as f:
            _CACHE = json.load(f)
    except json.JSONDecodeError:
        _CACHE = {}
else:
    _CACHE = {}


def _save_cache():
    """Persist cache to disk."""
    with open(CACHE_FILE, "w") as f:
        json.dump(_CACHE, f)


def get_geojson(year: int, url: str):
    """
    Cached GeoJSON loader (persistent disk cache).
    """

    key = f"{year}|{url}"

    if key in _CACHE:
        return _CACHE[key]

    print(f" Downloading GeoJSON for {year}")
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch GeoJSON: {response.status_code}")

    data = response.json()

    _CACHE[key] = data
    _save_cache()

    return data


def preload_years(years: list[int], world_by_year: dict):
    """
    Optional: preload all maps at startup.
    """
    for year in years:
        url = world_by_year.get(year)
        if url:
            get_geojson(year, url)

    _save_cache()