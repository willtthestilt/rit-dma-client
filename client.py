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


def get_trader(session):
    """Return the current trader state: trader_id, first name, last name, nlv,
    and total fines.
    """
    r = session.get(BASE + "/v1/trader", timeout=10)
    r.raise_for_status()
    return r.json()


def get_securities(session):
    """Return the current securities state: list of securities with their
    ticker, bid, ask, last, position, and volume.
    """
    r = session.get(BASE + "/v1/securities", timeout=10)
    r.raise_for_status()
    return r.json()


def get_book(session, ticker):
    """Return the order book for a security: a dict with bids and asks,
    each order carrying its price and quantity.
    """
    r = session.get(
        BASE + "/v1/securities/book",
        params={"ticker": ticker},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    s = make_session()
    case = get_case(s)
    trader = get_trader(s)
    securities = get_securities(s)
    book = get_book(s, "CRZY")
    print("tick:", case["tick"], "status:", case["status"])
    print(
        "trader_id:",
        trader["trader_id"],
        "first_name:",
        trader["first_name"],
        "last_name:",
        trader["last_name"],
        "nlv:",
        trader["nlv"],
        "total_fines:",
        trader["total_fines"],
    )
    print("securities:", securities)
    print("top bid:", book["bids"][0]["price"])
