"""Endpoints for basic debugging purposes.."""
from json import dumps
from . import END_POINT, DEBUG


@DEBUG.route(f"{END_POINT}/hello", methods=["GET"])
def hello():
    """Checks if connectivity exists."""
    return dumps({"message": "Hello, World!"})

