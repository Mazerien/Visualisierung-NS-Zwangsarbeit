import os
import requests


def get_directus_config():
    url = os.getenv("DIRECTUS_URL")
    token = os.getenv("DIRECTUS_TOKEN")

    if not url or not token:
        raise RuntimeError("Missing Directus env vars")

    return url, token


def get_headers():
    _, token = get_directus_config()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def directus_get(collection: str, cache_key: str):
    url_base, _ = get_directus_config()

    url = f"{url_base}/items/{collection}"

    params = {
        "filter[cache_key][_eq]": cache_key
    }

    r = requests.get(url, headers=get_headers(), params=params)
    r.raise_for_status()

    data = r.json().get("data", [])
    return data[0] if data else None

def directus_upsert(collection: str, payload: dict):
    existing = directus_get(collection, payload["cache_key"])

    url_base, _ = get_directus_config()

    if existing:
        item_id = existing["id"]
        url = f"{url_base}/items/{collection}/{item_id}"
        r = requests.patch(url, headers=get_headers(), json=payload)
    else:
        url = f"{url_base}/items/{collection}"
        r = requests.post(url, headers=get_headers(), json=payload)

    r.raise_for_status()
    return r.json()