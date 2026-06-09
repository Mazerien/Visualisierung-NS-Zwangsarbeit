from flask import Blueprint, jsonify
from person_data_country import get_nationality_counts

NATIONALITY = Blueprint("nationality", __name__)
END_POINT = "/api/nationality"
print("NATIONALITY MODULE LOADED")

@NATIONALITY.route(END_POINT, methods=["GET"])
def nationality_counts():
    print("NATIONALITY ROUTE CALLED")
    try:
        data = get_nationality_counts()
        return jsonify(data)

    except Exception as e:
        print("NATIONALITY ERROR:", e)
        return jsonify({}), 200