from os import getenv
from dotenv import load_dotenv

URL = "http://localhost:8055"
load_dotenv("../.env")
ADMIN_TOKEN = getenv("ADMIN_TOKEN")
AUTH_HEADER = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
