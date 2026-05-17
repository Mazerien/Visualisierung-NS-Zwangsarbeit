from flask import Blueprint, jsonify
from person_data_country import get_nationality_counts

NATIONALITY = Blueprint("nationality", __name__)
END_POINT = "/api/nationality"

@NATIONALITY.route(END_POINT, methods=["GET"])
def nationality_counts():
    data = get_nationality_counts()
    return jsonify(data)