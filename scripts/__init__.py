from dotenv import load_dotenv
from os import getenv

URL = "http://localhost:8055"
load_dotenv("../.env")
ADMIN_TOKEN = getenv("ADMIN_TOKEN")
AUTH_HEADER = {"Authorization": f"Bearer {ADMIN_TOKEN}"}