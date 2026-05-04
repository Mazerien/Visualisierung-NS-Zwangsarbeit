from backend.app import app
import pytest
import requests

URL = "http://localhost:5000"

def test_connection():
    res = requests.get(f"{URL}/api/hello")
    assert res.status_code == 200


def test_osm_no_params():
    res = requests.get(f"{URL}/api/osm")
    assert res.status_code == 200


def test_osm_params():
    res = requests.get(f"{URL}/api/osm?zoom_level=2")
    assert res.status_code == 200


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

