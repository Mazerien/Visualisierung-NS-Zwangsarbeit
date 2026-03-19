"""Flask backend with middleware from api/."""
from flask import Flask, Blueprint
from flask_cors import CORS
from api.debug import DEBUG
from api.osm import OSM
from api.ohm import OHM

app = Flask(__name__)
CORS(app=app)

middleware: list[Blueprint] = [DEBUG, OSM, OHM]
with app.app_context():
    for api in middleware:
        app.register_blueprint(api)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
