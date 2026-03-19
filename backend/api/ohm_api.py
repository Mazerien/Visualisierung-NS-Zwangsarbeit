from flask import Blueprint, request, jsonify
import requests

OHM_API = Blueprint("OHM_API", __name__)

OVERPASS_URL = "https://overpass-api.openhistoricalmap.org/api/interpreter"


@OHM_API.route("/api/ohm_api", methods=["GET"])
def api_ohm_city():
    """
    Get city coordinates and historical info from OpenHistoricalMap.

    Query parameters:
        - name: city name (required)
        - country: optional country filter
        - year: optional historical year filter

    Example:
        /api/ohm_api?name=Berlin
        /api/ohm_api?name=Berlin&country=Germany
        /api/ohm_api?name=Berlin&year=1800
    """

    city_name = request.args.get("name")
    country = request.args.get("country")
    year = request.args.get("year", type=int)

    if not city_name:
        return jsonify({"error": "City name is required"}), 400

    # -----------------------------
    # Build Overpass query
    # -----------------------------
    if country:
        query = f"""
        [out:json][timeout:25];
        area["name"="{country}"]["admin_level"="2"]->.searchArea;
        nwr["place"~"city|town|village"]["name"="{city_name}"](area.searchArea);
        out geom;
        """
    else:
        query = f"""
        [out:json][timeout:25];
        nwr["place"~"city|town|village"]["name"="{city_name}"];
        out geom;
        """

    # Apply historical filter if year provided
    if year:
        query = f"""
        [out:json][timeout:25];
        nwr["place"~"city|town|village"]["name"="{city_name}"](if:
            t["start_date"] < "{year + 1}" &&
            (!is_tag("end_date") || t["end_date"] >= "{year}")
        );
        out geom;
        """

    headers = {
        "User-Agent": "OHM-Python-Flask/1.0"
    }

    # -----------------------------
    # Call Overpass API (POST!)
    # -----------------------------
    try:
        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

    data = response.json()

    # -----------------------------
    # Process results
    # -----------------------------
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

    return jsonify(results)