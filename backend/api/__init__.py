"""
Flask blueprints for API.
"""
from flask import Blueprint

DEBUG_API = Blueprint("debug", __name__)
OSM_API = Blueprint("osm", __name__)