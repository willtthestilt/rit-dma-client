"""One-off probe confirming the DMA API exposes full order-book depth.

Kept as a record of how /v1/securities/book was found. Superseded once
client.get_book exists.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "http://flserver.rotman.utoronto.ca:16555"
HEADER = {"Authorization": os.environ["RIT_AUTH_HEADER"]}

r = requests.get(
    BASE + "/v1/securities/book",
    headers=HEADER,
    params={"ticker": "CRZY"},
    timeout=10,
)
print(r.status_code)
print(r.text[:600])
