"""
TODO: Docstring
"""
from flask import Blueprint, request, jsonify
from ohm import get_ohm_city_data
from . import END_POINT
OHM = Blueprint("OHM", __name__)


@OHM.route(f"{END_POINT}/ohm", methods=["GET"])
def api_ohm_city():
    """
    TODO: Docstring
    """
    city_name = request.args.get("name")
    country = request.args.get("country")
    year = request.args.get("year", type=int)

    if not city_name:
        return jsonify({"error": "City name is required"}), 400

    try:
        results = get_ohm_city_data(city_name, country, year)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
