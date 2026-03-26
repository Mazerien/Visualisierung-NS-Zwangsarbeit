import requests

OVERPASS_URL = "https://overpass-api.openhistoricalmap.org/api/interpreter"


def build_query(city_name, country=None, year=None):
    # Both country and year
    if country and year:
        return f"""
        [out:json][timeout:25];
        area["name"="{country}"]["admin_level"="2"]->.searchArea;
        nwr["place"]["name"~"^{city_name}$", i](area.searchArea)(if:
            t["start_date"] < "{year + 1}" &&
            (!is_tag("end_date") || t["end_date"] >= "{year}")
        );
        out geom;
        """

    # Only year
    if year:
        return f"""
        [out:json][timeout:25];
        nwr["place"]["name"~"^{city_name}$", i](if:
            t["start_date"] < "{year + 1}" &&
            (!is_tag("end_date") || t["end_date"] >= "{year}")
        );
        out geom;
        """

    # Only country
    if country:
        return f"""
        [out:json][timeout:25];
        area["name"="{country}"]["admin_level"="2"]->.searchArea;
        nwr["place"]["name"~"^{city_name}$", i](area.searchArea);
        out geom;
        """

    # Default: no filters
    return f"""
    [out:json][timeout:25];
    nwr["place"]["name"~"^{city_name}$", i];
    out geom;
    """


def fetch_data(query):
    headers = {
        "User-Agent": "OHM-Python-Flask/1.0"
    }

    response = requests.post(
        OVERPASS_URL,
        data={"data": query},
        headers=headers,
        timeout=60
    )
    response.raise_for_status()
    return response.json()


def process_results(data):
    results = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})

        coords = {}

        if "lat" in el and "lon" in el:
            coords = {"lat": el["lat"], "lon": el["lon"]}

        elif "geometry" in el and len(el["geometry"]) > 0:
            coords = {
                "lat": el["geometry"][0]["lat"],
                "lon": el["geometry"][0]["lon"]
            }

        results.append({
            "name": tags.get("name"),
            "coordinates": coords,
            "start_date": tags.get("start_date"),
            "end_date": tags.get("end_date")
        })

    return results


def get_ohm_city_data(city_name, country=None, year=None):
    query = build_query(city_name, country, year)
    data = fetch_data(query)
    return process_results(data)