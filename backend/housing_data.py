import requests
import os

TIMEOUT = 10

def get_directus_config():
    url = os.getenv("DIRECTUS_URL")
    token = os.getenv("DIRECTUS_TOKEN")

    if not url or not token:
        raise RuntimeError("Missing Directus env vars")

    return url, token


def extract_id(value):
    """
    Handles both:
    - 5
    - { "id": 5 }
    """
    if isinstance(value, dict):
        return value.get("id")
    return value


def get_housing_with_persons():
    directus_url, token = get_directus_config()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    housing_ids = [14, 26, 22, 41, 21]

    # -------------------------
    # HOUSING (_update)
    # -------------------------
    housing_res = requests.get(
        f"{directus_url}/items/housing_update",
        params={
            "filter[id][_in]": ",".join(map(str, housing_ids)),
            "fields": "id,name_place,type,foto.id,geo_coord"
        },
        headers=headers,
        timeout=TIMEOUT
    )

    housings = housing_res.json().get("data", [])

    # -------------------------
    # TENANCY (_update RELATIONS)
    # -------------------------
    tenancy_res = requests.get(
        f"{directus_url}/items/tenancy_update",
        params={
            "filter[housing_id][id][_in]": ",".join(map(str, housing_ids)),
            "fields": "housing_id.id,person_id.id"
        },
        headers=headers,
        timeout=TIMEOUT
    )

    tenancies_raw = tenancy_res.json().get("data", [])

    # Normalize tenancy data
    tenancies = []
    for t in tenancies_raw:
        hid = extract_id(t.get("housing_id"))
        pid = extract_id(t.get("person_id"))

        if hid is not None and pid is not None:
            tenancies.append({
                "housing_id": hid,
                "person_id": pid
            })

    # -------------------------
    # PERSONS (_update)
    # -------------------------
    person_ids = list({t["person_id"] for t in tenancies})

    if not person_ids:
        print("No person IDs found")
        return []

    person_res = requests.get(
        f"{directus_url}/items/person_update",
        params={
            "filter[id][_in]": ",".join(map(str, person_ids)),
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

    # -------------------------
    # GROUPING
    # -------------------------
    housing_map = {
        h["id"]: {
            **h,
            "persons": []
        }
        for h in housings
    }

    for t in tenancies:
        hid = t["housing_id"]
        pid = t["person_id"]

        if hid in housing_map and pid in person_map:
            housing_map[hid]["persons"].append(person_map[pid])

    # -------------------------
    # FINAL OUTPUT
    # -------------------------
    result = []

    for h in housing_map.values():
        # Geo handling
        geo = h.get("geo_coord")
        coords = None

        if isinstance(geo, dict) and "coordinates" in geo:
            lng, lat = geo["coordinates"]
            coords = [lat, lng]

        # File handling
        foto = None
        if isinstance(h.get("foto"), dict):
            file_id = h["foto"].get("id")
            if file_id:
                foto = f"{directus_url}/assets/{file_id}"

        result.append({
            "housing_id": h["id"],
            "name_place": h.get("name_place") or "Unknown place",
            "type": h.get("type") or "Unknown",
            "foto": foto,
            "coords": coords,
            "persons_count": len(set(h["persons"])),
            "persons": list(set(h["persons"]))
        })
    return result