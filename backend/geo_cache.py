"""
TODO: Docstring
"""
import json
import os
import requests

# -------------------------
# CONFIG
# -------------------------

GEONAMES_URL = "http://api.geonames.org/searchJSON"
GEONAMES_USERNAME = "PatrickProjekt"

OHM_URL = "http://localhost:5000/api/ohm"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "city_cache.json")

os.makedirs(CACHE_DIR, exist_ok=True)

# -------------------------
# LOAD CACHE
# -------------------------

if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="UTF-8") as f:
            _CACHE = json.load(f)
    except json.JSONDecodeError:
        _CACHE = {}
else:
    _CACHE = {}

# -------------------------
# HELPERS
# -------------------------

def _make_key(city_name: str, country: str, year: int) -> str:
    return f"{city_name.lower()}|{country.lower() if country else ''}|{year}"


def _save_cache():
    with open(CACHE_FILE, "w", encoding="UTF-8") as f:
        json.dump(_CACHE, f)


def _call_geonames(city_name: str, country: str = None):
    """GeoNames API call"""
    params = {
        "q": city_name,
        "maxRows": 1,
        "username": GEONAMES_USERNAME
    }

    if country:
        params["country"] = country

    r = requests.get(GEONAMES_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def _call_ohm(city_name: str, country: str = None, year: int = 1938):
    """OHM fallback API call"""
    params = {"name": city_name, "year": year}

    if country:
        params["country"] = country

    response = requests.get(OHM_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json()

# -------------------------
# MAIN FUNCTION
# -------------------------

def get_city_coords(city_name: str, country: str = None, year: int = 1938):
    """
    Unified geocoder:
    Cache → GeoNames → OHM → store result
    """

    key = _make_key(city_name, country, year)

    # 1. CACHE HIT
    if key in _CACHE:
        return _CACHE[key]

    coords = None
    source = None

    # 2. GEO NAMES FIRST (fast + modern)
    try:
        geo = _call_geonames(city_name, country)
        results = geo.get("geonames", [])

        if results:
            coords = [
                float(results[0]["lat"]),
                float(results[0]["lng"])
            ]
            source = "geonames"
    except TypeError:
        coords = None

    # 3. OHM FALLBACK (historical / fallback)
    if coords is None:
        try:
            data = _call_ohm(city_name, country, year)

            if isinstance(data, list) and len(data) > 0:
                for item in data:
                    c = item.get("coordinates")
                    if not c:
                        continue

                    coords = [c["lat"], c["lon"]]
                    source = "ohm"
                    break
        except KeyError:
            coords = None

    # 4. STORE RESULT (even if None)
    _CACHE[key] = {
        "coords": coords,
        "source": source
    }

    _save_cache()

    return _CACHE[key]

# -------------------------
# PRELOADING (optional)
# -------------------------

def preload_cities(cities: list[tuple]):
    """
    cities = [(city, country), ...]
    """
    for city, country in cities:
        get_city_coords(city, country)

    _save_cache()
