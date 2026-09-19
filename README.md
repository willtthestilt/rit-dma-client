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

Week 1 of an 8-week build.

**Working**
- Authenticated session handling, credentials read from environment
- Case state endpoint
- Order-book depth confirmed against a live case

**Planned**
- `get_book`, `get_trader`, `get_securities` moved into `client.py`
- Recorder writing timestamped book snapshots to JSONL
- Offline replay of recorded snapshots
- Market-making strategy: two-sided quoting with inventory limits
- Unit tests over strategy logic using fixture order books

## Setup

Requires Python 3.14 and access to a Rotman RIT account.
