"""
Flask backend with middleware from api/.
"""
import logging
from flask import Flask, Blueprint
from flask_cors import CORS
from api.debug import DEBUG
from api.osm import OSM
from api.ohm import OHM
from api.person_data_country_api import NATIONALITY
from api.housing_data_api import HOUSING
from flask import jsonify

def create_app() -> Flask:
    """
    Creates a Flask app and sets the logging.
    Also sets up API end points.
    """
    a = Flask(__name__)
    # Only log errors.
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    CORS(app=a)

    @a.errorhandler(404)
    def handle_404(e):
        return jsonify({
            "error": "Not Found",
            "message": str(e)
        }), 404

    @a.errorhandler(500)
    def handle_500(e):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500
    
    @a.route("/debug")
    def debug():
        return {
            "loaded": True
        }

    middleware: list[Blueprint] = [DEBUG, OSM, OHM, NATIONALITY, HOUSING]
    with a.app_context():
        for api in middleware:
            print(a.url_map)
            print("REGISTERING:", api)
            a.register_blueprint(api)
            print("After registry ",a.url_map)
    return a


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
