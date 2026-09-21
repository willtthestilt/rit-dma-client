# rit-dma-client

A Python client for the Rotman Interactive Trader (RIT) DMA REST API, built to
support algorithmic trading strategies against live simulated markets.

## Why DMA

Rotman's published Python tutorial targets the **Client REST API** on
`localhost:9999`, which routes through the RIT desktop application and requires
it to be running on the same machine.

This project targets the **DMA REST API** instead. DMA talks to the Rotman
server directly, which means lower latency, no dependency on the desktop client,
and the ability to run from any machine with network access.

The tutorial does not document the DMA endpoints, so they were located by
probing candidate paths and reading the response codes. `test_connection.py` and
`probe_book.py` are kept as the record of that process.

Endpoints confirmed working:

- `GET /v1/case` — case status, tick, period
- `GET /v1/securities` — top-of-book quotes and positions
- `GET /v1/securities/book?ticker=X` — full order-book depth
- `GET /v1/trader` — account details

## Design

HTTP access is isolated in `client.py` so that strategy logic never touches the
network directly. This keeps strategy code testable against recorded data with
no live connection, and means a change of API surface only affects one module.

## Status

**Working**
- Authenticated session handling, credentials read from environment
- Case, trader, securities, and order-book endpoints
- Order-book depth confirmed against a live case

**Planned**
- Recorder writing timestamped book snapshots to JSONL
- Offline replay of recorded snapshots
- Market-making strategy: two-sided quoting with inventory limits
- Unit tests over strategy logic using fixture order books

## Setup

Requires Python 3.14 and access to a Rotman RIT account.
```
python -m venv .venv
.venv\Scripts\activate
pip install requests python-dotenv
```

Create a `.env` file in the project root:

```
RIT_AUTH_HEADER=Basic <your base64 credentials>
```

The value is available from the API Info dialog in the RIT client. Credentials
are read from the environment at runtime and are never committed; `.env` is
gitignored.

Run the client's smoke test with a case active:

```
python client.py
```

## Files

| File                 | Purpose                                              |
| -------------------- | ---------------------------------------------------- |
| `client.py`          | API client. Session handling and endpoint functions. |
| `probe_book.py`      | One-off probe confirming order-book depth.           |
| `test_connection.py` | Initial endpoint discovery script.                   |
