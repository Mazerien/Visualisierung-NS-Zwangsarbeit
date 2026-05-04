import pytest
import requests

URL = "http://localhost:5000"

def test_connection():
    res = requests.get(f"{URL}/api/hello")
    assert res.status_code == 200


def test_osm_no_params():
    res = requests.get(f"{URL}/api/osm")
    assert res.status_code == 200