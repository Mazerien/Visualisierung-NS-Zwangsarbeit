import requests
import os

TIMEOUT = 10

def get_directus_config():
    url = os.getenv("DIRECTUS_URL")
    token = os.getenv("DIRECTUS_TOKEN")

    if not url or not token:
        raise RuntimeError("Missing Directus env vars")

    return url, token


def get_housing_with_persons():
    directus_url, token = get_directus_config()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    housing_ids = [17, 25, 22]

    # -------------------------
    # HOUSING
    # -------------------------
    housing_res = requests.get(
        f"{directus_url}/items/housing_update",
        params={
            "filter[id][_in]": ",".join(map(str, housing_ids)),
            "fields": "id,name_place,type,foto,geo_coord"
        },
        headers=headers,
        timeout=TIMEOUT
    )

    housings = housing_res.json().get("data", [])

   # -------------------------
    # TENANCY (FIXED FIELD NAMES)
    # -------------------------
    tenancy_res = requests.get(
        f"{directus_url}/items/tenancy_update",
        params={
            "filter[housing_id][_in]": ",".join(map(str, housing_ids)),
            "fields": "housing_id,person_id"
        },
        headers=headers,
        timeout=TIMEOUT
    )

    tenancies = tenancy_res.json().get("data", [])

    # -------------------------
    # PERSONS (FIXED FIELD NAME)
    # -------------------------
    person_ids = list({t["person_update"] for t in tenancies if t.get("person_update") is not None})

    person_res = requests.get(
        f"{directus_url}/items/person_update",
        params={
            "filter[id][_in]": ",".join(map(str, person_ids)) if person_ids else "0",
            "fields": "id,first_name,last_name"
        },
        headers=headers,
        timeout=TIMEOUT
    )

    persons = person_res.json().get("data", [])

    person_map = {
        p["id"]: f"{p.get('first_name','')} {p.get('last_name','')}".strip()
        for p in persons
    }

    # Group tenancies by housing
    housing_map = {h["id"]: {**h, "persons": []} for h in housings}

    for t in tenancies:
        hid = t.get("housing_update")
        pid = t.get("person_update")

        if hid in housing_map and pid in person_map:
            housing_map[hid]["persons"].append(person_map[pid])

    # -------------------------
    # FINAL OUTPUT (FRONTEND SAFE CONTRACT)
    # -------------------------
    result = []

    for h in housing_map.values():
        geo = h.get("geo_coord")

        coords = None
        if geo and "coordinates" in geo:
            lng, lat = geo["coordinates"]
            coords = [lat, lng]
            
        result.append({
            "housing_id": h["id"],
            "name_place": h.get("name_place") or "Unknown place",
            "type": h.get("type") or "Unknown",
            "foto": h.get("foto") or None,
            "coords": coords,
            "persons_count": len(set(h["persons"])),
            "persons": list(set(h["persons"]))
        })

    return result