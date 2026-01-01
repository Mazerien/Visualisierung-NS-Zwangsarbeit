"""
Starts the Flask app and listens in on TCP/5000.
Also tries establishing connection with a pre-existing MySQL database.
"""
from os import getenv
from dotenv import load_dotenv

from flask import Flask, Blueprint
from flask_cors import CORS

from backend.database import MySQL
from backend.api.debug import DEBUG_API
from backend.api.osm import OSM_API

app = Flask(__name__)
CORS(app=app)

#######################################################################################
# MySQL Config                                                                        #
#######################################################################################
load_dotenv()
SQL_DB = getenv("SQL_DB")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")
SQL_HOST = getenv("SQL_HOST")
database = MySQL(
    user=SQL_USER, password=SQL_PASSWORD, host=SQL_HOST, db=SQL_DB
)
database.check_tables()


#######################################################################################
# Middleware                                                                          #
#######################################################################################
# TODO: Handle all DB CRUD requests here.
middleware: list[Blueprint] = [DEBUG_API, OSM_API]
with app.app_context():
    for api in middleware:
        app.register_blueprint(api)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
