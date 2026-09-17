import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "http://flserver.rotman.utoronto.ca:16555"
USER = os.environ["RIT_USERNAME"]
PASSWORD = os.environ["RIT_PASSWORD"]

PATHS = [
    "/v1/case",
    "/case",
    "/v1/securities",
    "/v1/trader",
]

for path in PATHS:
    url = BASE + path
    try:
        r = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        print(r.status_code, path)
        print("   ", r.text[:200])
    except requests.exceptions.RequestException as e:
        print("ERROR", path, type(e).__name__)
    print()
