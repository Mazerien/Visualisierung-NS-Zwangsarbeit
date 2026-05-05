"""
Flask blueprints.
"""
from flask import Blueprint

END_POINT = "/api"

DEBUG = Blueprint("debug", __name__)
OSM = Blueprint("osm", __name__)
OHM = Blueprint("ohm", __name__)
