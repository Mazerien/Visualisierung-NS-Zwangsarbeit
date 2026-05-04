import pytest
import requests

URL = "https://flask.p-qsvcne.project.space"

def test_connection():
    res = requests.get(f"{URL}/api/hello")
    assert res.status_code == 200


def test_osm_no_params():
    res = requests.get(f"{URL}/api/osm")
    assert res.status_code == 200


def test_osm_params():
    res = requests.get(f"{URL}/api/osm?zoom_level=2")
    assert res.status_code == 200

