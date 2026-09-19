"""Client for the Rotman Interactive Trader DMA REST API.

Wraps the authenticated HTTP calls to flserver so that strategy code
never touches the network directly. Credentials are read from .env.
"""

import os
import requests
from dotenv import load_dotenv

BASE = "http://flserver.rotman.utoronto.ca:16555"


def make_session():
    """Build an authenticated requests Session for the DMA API.

    Reads RIT_AUTH_HEADER from .env and attaches it to the session so
    every request made through it carries the header.
    """
    load_dotenv()
    session = requests.Session()
    session.headers.update({"Authorization": os.environ["RIT_AUTH_HEADER"]})
    return session


def get_case(session):
    """Return the current case state: tick, status, period, and limits."""
    r = session.get(BASE + "/v1/case", timeout=10)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    s = make_session()
    case = get_case(s)
    print("tick:", case["tick"], "status:", case["status"])
