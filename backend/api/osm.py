"""
Get the map from the backend.
"""
from flask import Blueprint, request, Response

from geo_map import OSMGeoMap
from arrows import get_arrows
from geo_cache import get_city_coords

OSM = Blueprint("osm", __name__)
END_POINT = "/api/osm"

def warm_cache(arrows):
    """
    Preload OHM coordinates into cache.
    """
    for start_city, start_country, end_city, end_country, _, _, _, _ in arrows:
        # Only preload start city
        _ = get_city_coords(start_city, country=start_country)
        # Optionally preload Schwenningen once
        _ = get_city_coords(end_city, country=end_country)


@OSM.route(END_POINT, methods=["GET"])
def get_map():
    """
    TODO: Docstring
    """
    # Get params
    zoom_level = int(request.args.get("zoom_level", 0))
    year = int(request.args.get("year", 1938))
    arrow_set = request.args.get("arrows", "default")

    # Load arrows dynamically
    arrows = get_arrows(arrow_set)

    warm_cache(arrows)

    # Generate map
    html_map = OSMGeoMap(
        zoom_level=zoom_level,
        arrows=arrows,
        year=year
    ).get_map()

    return Response(html_map, mimetype="text/html")
