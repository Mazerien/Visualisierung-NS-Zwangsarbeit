"""
TODO: Add docstring
"""
from flask import Flask, render_template
from os import getenv
from database import PSQL

app = Flask(__name__)

# PostgreSQL config
# TODO: WIP
PSQL_DB = getenv("PSQL_DB")
PSQL_USER = getenv("PSQL_USER")
PSQL_PASSWORD = getenv("PSQL_PASSWORD")
database = PSQL(
    user=PSQL_USER, password=PSQL_PASSWORD, db=PSQL_DB
)


@app.route("/")
def index():
    """
    TODO: Docstring
    """
    return render_template("index.html")