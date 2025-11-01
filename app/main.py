"""
Starts the Flask app and listens in on TCP/5000.
Also tries establishing connection with a pre-existing PostgreSQL database.
"""
from flask import Flask, render_template, request
from os import getenv
from database import PSQL
from map import draw_map_from_place


app = Flask(__name__)

#######################################################################################
# PostgreSQL Config                                                                   #
#######################################################################################
PSQL_DB = getenv("PSQL_DB")
PSQL_USER = getenv("PSQL_USER")
PSQL_PASSWORD = getenv("PSQL_PASSWORD")
database = PSQL(
    user=PSQL_USER, password=PSQL_PASSWORD, db=PSQL_DB
)
# TODO: Working PostgreSQL database
try:
    database.create_table()
except Exception as e:
    print(e)
    print("No PostgreSQL connection possible. Continuing.")


#######################################################################################
# Routing                                                                             #
#######################################################################################
@app.route("/")
def index():
    """
    TODO: Docstring
    """
    return render_template("index.html")


@app.route("/map", methods=["GET", "POST"])
def map():
    """
    Handles map rendering. 
    Stores an image within static/images/ and displays it after finishing rendering.
    """
    if request.method == "POST":
        city = request.form["city"]
        area = request.form["area"]
        country = request.form["country"]
        app.logger.info(
            f"Sending OSM API request about {city}, {area}, {country}...")
        draw_map_from_place(f"{city}, {area}, {country}")
        return render_template("map.html")

    # TODO: Add it so if there is no POST request, no image is shown
    # TODO: Also check for lack of an image altogether (shows error image as of now)
    return render_template("map.html")
