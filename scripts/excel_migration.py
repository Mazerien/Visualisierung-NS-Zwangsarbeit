"""Script to migrate data from the .xlsx into Directus."""
# TODO
import requests
from dotenv import load_dotenv
from os import getenv

URL = "http://localhost:8055"
load_dotenv("../.env")
ADMIN_TOKEN = getenv("ADMIN_TOKEN")

def test_connection() -> int:
    return requests.get(URL).status_code


def authenticate():
    pass


def main():
    if test_connection() != 200:
        print("No connection possible. Is Directus running?")
        return
    pass


if __name__ == "__main__":
    main()
    print(requests.post(f"{URL}/collections", data={"collection": "test"}, headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}))