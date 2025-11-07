"""
Starts the Flask app and listens in on TCP/5000.
Also tries establishing connection with a pre-existing MySQL database.
"""
from flask import Flask, render_template, request
from os import getenv
from database import MySQL
from geography import draw_map_from_place


app = Flask(__name__)

#######################################################################################
# MySQL Config                                                                        #
#######################################################################################
SQL_DB = getenv("SQL_DB")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")
SQL_HOST = getenv("SQL_HOST")
database = MySQL(
    user=SQL_USER, password=SQL_PASSWORD, host=SQL_HOST, db=SQL_DB
)


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

    # TODO: Add it so if there is no POST request, no image is shown
    # TODO: Also check for lack of an image altogether (shows error image as of now)
    return render_template("map.html")


@app.route("/data", methods=["GET", "POST"])
def data():
    """
    Graphical interface for the MySQL database.
    POST requests create new demo data.
    """
    # TODO: More interaction capabilities
    if request.method == "POST":
        database.create_demo_data()
    return render_template("database.html", columns=database.get_columns_in_table("person"), rows=database.get_rows_in_table("person"))
