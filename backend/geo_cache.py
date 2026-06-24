"""
TODO: Docstring
"""
import json
import os
import requests
from directusHelper import directus_get, directus_upsert
from mapper.country_map import COUNTRY_ALIASES
from mapper.country_bbox_map import COUNTRY_BBOX

# -------------------------
# CONFIG
# -------------------------

GEONAMES_URL = "http://api.geonames.org/searchJSON"
GEONAMES_USERNAME = "PatrickProjekt"

OHM_URL = "https://flask.p-qsvcne.project.space/api/ohm"
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

def _in_bbox(lat: float, lng: float, bbox):
    if not bbox:
        return False

    south, north, west, east = bbox
    return south <= lat <= north and west <= lng <= east

def resolve_country_code(country_name: str | None):
    if not country_name:
        return None

    c = country_name.strip().lower()

    # already ISO code
    if len(c) == 2 and c.isalpha():
        return c.upper()

    return COUNTRY_ALIASES.get(c)

def _make_key(city_name: str, country: str = None) -> str:
    return f"{city_name.lower().strip()}|{country.lower().strip() if country else ''}"


def _save_cache():
    with open(CACHE_FILE, "w", encoding="UTF-8") as f:
        json.dump(_CACHE, f)


def _clean_city(city_name: str) -> str:
    if not city_name:
        return ""
    return city_name.strip().lower()


def _is_valid_city(city_name: str) -> bool:
    cleaned = _clean_city(city_name)
    return cleaned not in ["", "unknown", "n/a", "null", "none"]


# -------------------------
# API CALLS
# -------------------------

def _call_geonames(city_name: str, country: str = None):
    params = {
        "q": city_name,
        "maxRows": 10,
        "username": GEONAMES_USERNAME,
        "featureClass": "P",
    }

    country_code = resolve_country_code(country)
    if country_code:
        params["country"] = country_code

    r = requests.get(
        "http://api.geonames.org/searchJSON",
        params=params,
        timeout=20
    )
    r.raise_for_status()
    return r.json()


def _call_ohm(city_name: str, country: str = None, year: int = None):
    params = {"name": city_name}

    if country:
        params["country"] = country
    if year:
        params["year"] = year

    r = requests.get(OHM_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


# -------------------------
# SCORING ENGINE
# -------------------------

def _score_geonames(item, city, country=None):
    score = 0

    name = (item.get("name") or "").lower()
    country_code = (item.get("countryCode") or "").upper()

    # -------------------------
    # NAME MATCHING
    # -------------------------
    if name == city:
        score += 60
    elif name.startswith(city):
        score += 30

    # -------------------------
    # COUNTRY MATCH
    # -------------------------
    if country:
        resolved = resolve_country_code(country)
        if resolved and country_code == resolved:
            score += 50
        else:
            score -= 10

    # -------------------------
    # POPULATED PLACE BOOST
    # -------------------------
    if item.get("fcl") == "P":
        score += 10

    # -------------------------
    # POPULATION BIAS
    # -------------------------
    try:
        score += min(int(item.get("population", 0)) / 100000, 10)
    except Exception:
        pass

    # -------------------------
    #  BOUNDING BOX BIAS
    # -------------------------
    if country:
        resolved = resolve_country_code(country)
        bbox = COUNTRY_BBOX.get(resolved)

        try:
            lat = float(item["lat"])
            lng = float(item["lng"])

            if bbox:
                if _in_bbox(lat, lng, bbox):
                    score += 40   # strong boost
                else:
                    score -= 25   # strong penalty
        except Exception:
            pass

    return score


def _score_ohm(item, city, country=None):
    score = 0

    name = (item.get("name") or "").lower()

    if name == city:
        score += 60
    elif city in name:
        score += 25

    c = item.get("coordinates")
    if not c:
        return -999

    # OHM is historical -> weaker country enforcement
    if country and item.get("country", "").lower() == country.lower():
        score += 20

    if country:
        resolved = resolve_country_code(country)
        bbox = COUNTRY_BBOX.get(resolved)

        c = item.get("coordinates")
        if bbox and c:
            if _in_bbox(c["lat"], c["lon"], bbox):
                score += 20
            else:
                score -= 10
    return score


def _pick_best(candidates):
    if not candidates:
        return None

    return max(candidates, key=lambda x: x["score"])


# -------------------------
# MAIN FUNCTION
# -------------------------

def get_city_coords(city_name: str, country: str = None, year: int = 1938):

    if not _is_valid_city(city_name):
        return {"coords": None, "source": "invalid_city", "confidence": 0}

    key = _make_key(city_name, country)

    # -------------------------
    # DIRECTUS CACHE
    # -------------------------
    cached = directus_get("CityGeoData", key)
    if cached:
        return {
            "coords": cached.get("coords"),
            "source": cached.get("source"),
            "confidence": cached.get("confidence", 1.0)
        }

    city_clean = _clean_city(city_name)

    candidates = []

    # -------------------------
    # 1. GEO NAMES
    # -------------------------
    try:
        geo = _call_geonames(city_name, country)
        for item in geo.get("geonames", []):
            coords = None
            try:
                coords = [float(item["lat"]), float(item["lng"])]
            except Exception:
                continue

            candidates.append({
                "coords": coords,
                "source": "geonames",
                "score": _score_geonames(item, city_clean, country)
            })
    except Exception:
        pass

    # -------------------------
    # 2. GEO NAMES (no country fallback)
    # -------------------------
    if not candidates:
        try:
            geo = _call_geonames(city_name, None)
            for item in geo.get("geonames", []):
                try:
                    coords = [float(item["lat"]), float(item["lng"])]
                except Exception:
                    continue

                candidates.append({
                    "coords": coords,
                    "source": "geonames_no_country",
                    "score": _score_geonames(item, city_clean, country)
                })
        except Exception:
            pass

    # -------------------------
    # 3. OHM (with context)
    # -------------------------
    try:
        data = _call_ohm(city_name, country, year)
        for item in data:
            c = item.get("coordinates")
            if not c:
                continue

            candidates.append({
                "coords": [c["lat"], c["lon"]],
                "source": "ohm",
                "score": _score_ohm(item, city_clean, country)
            })
    except Exception:
        pass

    # -------------------------
    # 4. OHM (no constraints)
    # -------------------------
    if not candidates:
        try:
            data = _call_ohm(city_name, None, None)
            for item in data:
                c = item.get("coordinates")
                if not c:
                    continue

                candidates.append({
                    "coords": [c["lat"], c["lon"]],
                    "source": "ohm_no_context",
                    "score": _score_ohm(item, city_clean, country)
                })
        except Exception:
            pass

    # -------------------------
    # PICK BEST RESULT
    # -------------------------
    best = _pick_best(candidates)

    if best:
        coords = best["coords"]
        source = best["source"]
        confidence = round(min(best["score"] / 100, 1.0), 3)
    else:
        coords = None
        source = "not_found"
        confidence = 0

    # -------------------------
    # STORE IN DIRECTUS
    # -------------------------
    payload = {
        "city": city_name,
        "country": country,
        "year": year,
        "coords": coords,
        "source": source,
        "confidence": confidence,
        "cache_key": key
    }

    directus_upsert("CityGeoData", payload)

    return {
        "coords": coords,
        "source": source,
        "confidence": confidence
    }


# -------------------------
# PRELOADING
# -------------------------

def preload_cities(cities: list[tuple]):
    for city, country in cities:
        get_city_coords(city, country)

    _save_cache()