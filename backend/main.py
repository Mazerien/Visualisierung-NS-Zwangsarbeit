"""
Starts the Flask app and listens in on TCP/5000.
Also tries establishing connection with a pre-existing MySQL database.
"""
from os import getenv
from dotenv import load_dotenv

from flask import Flask, render_template, request
from flask_cors import CORS
from database import MySQL
from geography import web_map, get_folium_map


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


#######################################################################################
# Routing                                                                             #
#######################################################################################
@app.route("/")
def index():
    """
    TODO: Docstring
    """
    return render_template("index.html")


@app.route("/map", methods=["GET"])
def map():
    """
    Handles map rendering through an embedded and rendered iframe using OpenStreetMap. 
    Can be used with request parameters.
    """
    osm_map = None
    if request.args.get("city"):
        city = request.args.get("city")
        area = request.args.get("area")
        country = request.args.get("country")
        app.logger.info(
            f"Sending OSM API request about {city}, {area}, {country}...")
        #osm_map = web_map(f"{city}, {area}, {country}")
        osm_map = get_folium_map()

        # TODO: Think about way to style this
        osm_map.get_root().width = "60%"
        osm_map = osm_map.get_root()._repr_html_()
    # TODO: Also check for lack of an image altogether (shows error image as of now)
    return render_template("map.html", web_map=osm_map)


@app.route("/data", methods=["GET", "POST"])
def data():
    """
    Graphical interface for the MySQL database.
    POST requests create new demo data.
    """
    # TODO: More interaction capabilities
    if request.method == "POST":
        database.drop_tables()
    return render_template("database.html", columns=database.select_columns_in_table("Person"),
                           rows=database.select_rows_in_table("Person"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
