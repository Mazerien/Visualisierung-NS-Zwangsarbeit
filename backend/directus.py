"""
!!Very WIP!!
Integration of Directus into the Flask backend.
"""
import asyncio
from directus_sdk_py import DirectusClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()
DIRECTUS_EMAIL = getenv("DIRECTUS_EMAIL")
DIRECTUS_PASSWORD = getenv("DIRECTUS_PASSWORD")

def main():
    client = DirectusClient("http://localhost:8055", email=DIRECTUS_EMAIL, password=DIRECTUS_PASSWORD)
    #client.login
    response = client.get_collection("directus_users")
    print(
        client.me()
    )
    client.logout()
    #client.close_connection()
    #directus = 


if __name__ == "__main__":
    main()

