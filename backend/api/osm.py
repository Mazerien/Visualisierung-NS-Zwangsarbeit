"""
Get the map from the backend.
"""
from json import dumps
from flask import render_template, request

from backend.geography import get_folium_map
from backend.osm import OSM
from . import OSM_API

END_POINT = "/api/osm"

@OSM_API.route(END_POINT, methods=["GET"])
def api_map():
    """
    Handles map rendering through an embedded and rendered iframe using OpenStreetMap. 
    Can be used with request parameters.
    TODO Markers with people
    """
    osm = OSM(tileset="cartodbpositron", zoom_level=0)
    return osm.get_map()