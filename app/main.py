"""
TODO: Add docstring
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """
    TODO: Docstring
    """
    return render_template("index.html")