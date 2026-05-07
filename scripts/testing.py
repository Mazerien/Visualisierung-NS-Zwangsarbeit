"""
Uses a Flask application factory to test its own API end points in a localhost environment.
"""
import pytest
import sys
from flask import Flask

sys.path.append("../backend")
from backend.app import create_app

URL = "http://localhost:5000"


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


def test_connection(client):
    res = client.get(f"{URL}/api/hello")
    assert res.status_code == 200


def test_osm_no_params(client):
    res = client.get(f"{URL}/api/osm")
    assert res.status_code == 200


def test_osm_params(client):
    res = client.get(f"{URL}/api/osm?zoom_level=2")
    assert res.status_code == 200

