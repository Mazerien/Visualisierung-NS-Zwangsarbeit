"""
Basic debugging.
"""
from json import dumps
from flask import render_template
from . import DEBUG_API

END_POINT = "/api"


@DEBUG_API.route("/")
def api_index():
    """
    Overview of Flask app for debugging purposes.
    """
    return render_template("index.html")


@DEBUG_API.route(f"{END_POINT}/hello", methods=["GET"])
def api_hello():
    """
    Basic function to ensure connectivity.
    """
    return dumps({"message": "Hello, World!"})
