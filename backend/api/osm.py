"""Get the map from the backend."""
from json import dumps
from . import END_POINT, OSM

END_POINT += "/osm"

@OSM.route(END_POINT, methods=["GET"])
def get_map():
    # TODO
    return dumps({"TODO": "Create map"})