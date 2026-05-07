"""
Uses a Flask application factory to test its own API end points in a localhost environment.
"""
import pytest
import sys
from flask import Flask

sys.path.append("../backend")
from backend.app import create_app

# With testing from GitHub,
# rate limiting is a high possibility.
# For these cases, a 500 instead of a 200 response is acceptable.

URL = "http://localhost:5000"

### Set up Flask
@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def runner(app: Flask):
    return app.test_cli_runner()


### Unit Tests
def test_connection(client):
    res = client.get(f"{URL}/api/hello")
    assert res.status_code == 200
    assert b"Hello, World!" in res.data


def test_osm_no_params(client):
    res = client.get(f"{URL}/api/osm")
    assert res.status_code == 200 or res.status_code == 500


def test_osm_params(client):
    res = client.get(f"{URL}/api/osm?zoom_level=2")
    assert res.status_code == 200 or res.status_code == 500


def test_osm_no_params(client):
    res = client.get(f"{URL}/api/osm")
    assert res.status_code == 200 or res.status_code == 500


def test_ohm_city_no_params(client):
    res = client.get(f"{URL}/api/ohm")
    assert res.status_code == 400


def test_ohm_city_city(client):
    res = client.get(f"{URL}/api/ohm?name=Berlin")
    assert res.status_code == 200 or res.status_code == 500