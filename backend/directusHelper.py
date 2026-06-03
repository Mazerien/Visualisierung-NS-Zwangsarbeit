import os
import requests

DIRECTUS_URL = os.getenv("DIRECTUS_URL")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {DIRECTUS_TOKEN}",
    "Content-Type": "application/json"
}


def directus_get(collection: str, cache_key: str):
    url = f"{DIRECTUS_URL}/items/{collection}"
    print("TOKEN:", repr(DIRECTUS_TOKEN))
    print("URL:", DIRECTUS_URL)
    params = {
        "filter[cache_key][_eq]": cache_key
    }

    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()

    data = r.json().get("data", [])
    return data[0] if data else None

def directus_upsert(collection: str, payload: dict):
    existing = directus_get(collection, payload["cache_key"])

    if existing:
        item_id = existing["id"]
        url = f"{DIRECTUS_URL}/items/{collection}/{item_id}"
        r = requests.patch(url, headers=HEADERS, json=payload)
    else:
        url = f"{DIRECTUS_URL}/items/{collection}"
        r = requests.post(url, headers=HEADERS, json=payload)

    r.raise_for_status()
    return r.json()