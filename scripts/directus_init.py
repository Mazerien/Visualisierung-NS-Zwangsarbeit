"""Script to migrate data from the .xlsx into Directus."""
# TODO
import json
import requests
from os import listdir
from __init__ import URL, AUTH_HEADER
from migrate_data import MigrateData


def test_connection() -> int:
    """Checks if Directus is online."""
    return requests.get(URL).status_code


def test_authentication() -> int:
    """Quick check if logging in with the admin token is possible. Refer to .env in project root."""
    return requests.get(f"{URL}/collections", headers=AUTH_HEADER).status_code


def create_collections():
    """Goes through every schema and creates a Directus collection for them."""
    directory = "schema"
    collections = [f for f in listdir(directory)]
    for collection in collections:
        with open(f"{directory}/{collection}") as f:
            payload = json.load(f)
            req = requests.post(f"{URL}/collections", json=payload,
                                headers=AUTH_HEADER)
            print(req.content)


def drop_tables():
    """Optionally soft resets the Directus DB."""
    req = requests.delete(f"{URL}/items/Person", params={"filter[FirstName][_nempty]": ""}, headers=AUTH_HEADER)
    print(req.status_code)
    print(req.reason)
    print(req.content)


def main():
    if test_connection() != 200:
        raise "No connection possible. Is Directus running?"
    elif test_authentication() != 200:
        raise "Directus cannot authenticate with the given admin token. Is the .env set correctly?"
    
    # while True:
    #     reset = input("Reset Directus database? y/N\n")
    #     match reset.lower():
    #         case "" | "n": break
    #         case "y" | "j": drop_tables()

    while True:
        collections = input("Create Directus Collections? y/N\n")
        match collections.lower():
            case "" | "n": break
            case "y" | "j":
                create_collections()
                break

    while True:
        items = input("Create Directus items from .xlsx data? y/N\n")
        match items.lower():
            case "" | "n": break
            case "y" | "j":
                MigrateData.migrate()
                break


if __name__ == "__main__":
    main()
