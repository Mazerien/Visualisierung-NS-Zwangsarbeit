"""Flask blueprints."""
from flask import Blueprint

END_POINT = "/api"

DEBUG = Blueprint("debug", __name__)
OSM = Blueprint("osm", __name__)
