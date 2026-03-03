"""Flask blueprints."""
from flask import Blueprint

DEBUG = Blueprint("debug", __name__)
OSM = Blueprint("osm", __name__)
END_POINT = "/api"