"""TODO: Docstring"""
from flask import Blueprint, jsonify
from housing_data import get_housing_with_persons

HOUSING = Blueprint("housing", __name__)
END_POINT = "/api/housing-persons"

@HOUSING.route(END_POINT, methods=["GET"])
def housing_persons():
    """TODO: Docstring"""
    try:
        data = get_housing_with_persons()
        return jsonify(data)
    except Exception as e:
        print("HOUSING ERROR:", e)
        return jsonify([]), 200
