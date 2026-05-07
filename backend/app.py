"""
Flask backend with middleware from api/.
"""
import logging
from flask import Flask, Blueprint
from flask_cors import CORS
from api.debug import DEBUG
from api.osm import OSM
from api.ohm import OHM


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

    middleware: list[Blueprint] = [DEBUG, OSM, OHM]
    with a.app_context():
        for api in middleware:
            a.register_blueprint(api)
    return a


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
