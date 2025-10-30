"""
TODO: Add docstring
"""
from flask import Flask, render_template
from os import getenv
from postgres import SQL

app = Flask(__name__)

# PostgreSQL config
# TODO: WIP
DB_HOST = getenv("POSTGRES_DB")
DB_USER = getenv("POSTGRES_USER")
DB_PASSWORD = getenv("POSTGRES_PASSWORD")
database = SQL(
    user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=5432
)


@app.route("/")
def index():
    """
    TODO: Docstring
    """
    return render_template("index.html")