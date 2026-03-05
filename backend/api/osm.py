"""Get the map from the backend."""
from json import dumps
from flask import request
from . import END_POINT, OSM
from osm import OpenStreetMap

END_POINT += "/osm"


@OSM.route(END_POINT, methods=["GET"])
def get_map():
    zoom_level = request.args.get("zoom_level")
    return dumps({"map": str(OpenStreetMap(zoom_level))})
