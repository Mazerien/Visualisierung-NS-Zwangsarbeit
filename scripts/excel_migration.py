"""Script to migrate data from the .xlsx into Directus."""
# TODO
import json
import requests
from dotenv import load_dotenv
from os import getenv, listdir

URL = "http://localhost:8055"
load_dotenv("../.env")
ADMIN_TOKEN = getenv("ADMIN_TOKEN")


def test_connection() -> int:
    return requests.get(URL).status_code


def test_authentication() -> int:
    with open("schema/Person.json") as f:
        payload = json.load(f)
        return requests.post(f"{URL}/collections", json=payload, headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}).status_code


def create_collections():
    """Goes through every schema and creates a Directus collection for them."""
    directory = "schema"
    collections = [f for f in listdir(directory)]
    for collection in collections:
        with open(f"{directory}/{collection}") as f:
            payload = json.load(f)
            requests.post(f"{URL}/collections", json=payload,
                          headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})


def main():
    if test_connection() != 200:
        raise "No connection possible. Is Directus running?"
    # elif test_authentication() != 200:
    #    raise "Directus cannot authenticate with the given admin token. Is the .env set correctly?"
    create_collections()


if __name__ == "__main__":
    main()
