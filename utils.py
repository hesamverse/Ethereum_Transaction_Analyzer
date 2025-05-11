#!/usr/bin/env python3
"""Utility helpers for Ethereum Transaction Analyzer."""

from __future__ import annotations

import os
from datetime import datetime
from typing import List, Dict

import matplotlib
matplotlib.use("Agg")        # Safe backend for headless/terminal runs
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY: str | None = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"


def fetch_transactions(address: str) -> List[Dict]:
    """Return full tx‑history for *address* via the Etherscan API."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 999_999_99,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY,
    }
    resp = requests.get(ETHERSCAN_BASE_URL, params=params, timeout=15)
    data = resp.json()

    # Explicit error handling
    if data["status"] != "1":
        msg = data.get("message", "UNKNOWN")
        if msg == "NOTOK" and "rate limit" in data.get("result", "").lower():
            raise RuntimeError("Etherscan rate‑limited — try again shortly.")
        raise RuntimeError(f"Etherscan error: {msg} ({data.get('result')})")

    return data["result"]


def convert_timestamp(unix_ts: str | int) -> str:
    """Convert UNIX epoch (seconds) → human‑readable UTC string."""
    try:
        ts = int(unix_ts)
        return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return "Invalid"


def plot_gas_usage(transactions: List[Dict]) -> None:
    """Line‑chart of gas usage per tx."""
    if not transactions:
        return

    dates = [convert_timestamp(tx["timeStamp"])[:10] for tx in transactions]
    gas_vals = [int(tx["gasUsed"]) for tx in transactions]

    plt.figure(figsize=(12, 5))
    plt.plot(dates, gas_vals, marker="o", linewidth=2)
    plt.xticks(rotation=45)
    plt.title("⛽ Gas Usage Over Time")
    plt.tight_layout()
    plt.grid(True)
    plt.show(block=False)


def plot_top_interactions(transactions: List[Dict], top_n: int = 5) -> None:
    """Pie‑chart of top‑N interacted addresses."""
    if not transactions:
        return

    from collections import Counter

    counter = Counter(tx["to"] for tx in transactions if tx["to"])
    if not counter:
        return

    labels, counts = zip(*counter.most_common(top_n))
    labels = [addr[:8] + "…" for addr in labels]

    others = sum(counter.values()) - sum(counts)
    if others:
        labels += ("Others",)
        counts += (others,)

    plt.figure(figsize=(7, 7))
    plt.pie(counts, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("🤝 Interaction Distribution")
    plt.axis("equal")
    plt.tight_layout()
    plt.show(block=False)
