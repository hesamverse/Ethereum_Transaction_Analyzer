#!/usr/bin/env python3
"""
CLI entry point for Ethereum Transaction Analyzer.

Example:
    python analyzer.py 0xABC... --limit 20 --no-gas-graph
"""

import argparse
from typing import List, Dict

from rich.console import Console
from rich.table import Table

from utils import (
    fetch_transactions,
    convert_timestamp,
    plot_gas_usage,
    plot_top_interactions,
)

console = Console()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="🔍 Ethereum Transaction Analyzer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("address", help="Ethereum address (0x…) to analyze")
    parser.add_argument(
        "--limit", type=int, default=10, help="Number of recent txs to display"
    )
    parser.add_argument("--no-gas-graph", action="store_true", help="Disable gas chart")
    parser.add_argument("--no-pie", action="store_true", help="Disable pie chart")
    return parser.parse_args()


def analyze_transactions(transactions: List[Dict]) -> tuple[float, str, int]:
    """Return (avg_gas, top_address, count) for a tx list."""
    total_gas = 0
    interactions: dict[str, int] = {}

    for tx in transactions:
        gas = int(tx["gasUsed"])
        total_gas += gas

        to_addr = tx["to"]
        if to_addr:
            interactions[to_addr] = interactions.get(to_addr, 0) + 1

    avg = total_gas / len(transactions) if transactions else 0
    top_addr = max(interactions, key=interactions.get) if interactions else "N/A"
    top_count = interactions.get(top_addr, 0)
    return avg, top_addr, top_count


def display_table(transactions: List[Dict], limit: int) -> None:
    """Pretty‑print transaction table."""
    table = Table(title=f"📄 Latest {limit} Transactions", show_lines=True)
    table.add_column("Hash", style="bold magenta")
    table.add_column("From", style="dim")
    table.add_column("To", style="dim")
    table.add_column("Gas", justify="right", style="yellow")
    table.add_column("Date", style="green")

    for tx in transactions[:limit]:
        table.add_row(
            tx["hash"][:10] + "…",
            tx["from"][:10] + "…",
            tx["to"][:10] + "…",
            f"{int(tx['gasUsed']):,}",
            convert_timestamp(tx["timeStamp"]),
        )

    console.print(table)


def main() -> None:
    args = parse_arguments()

    if not (args.address.startswith("0x") and len(args.address) == 42):
        console.print("❌ Invalid Ethereum address supplied.")
        return

    try:
        txs = fetch_transactions(args.address)
    except Exception as exc:
        console.print(f"🚨 {exc}")
        return

    if not txs:
        console.print("🚫 No transactions found.")
        return

    avg_gas, top_addr, top_cnt = analyze_transactions(txs)
    console.print(f"⛽ Average Gas: {avg_gas:,.2f}")
    console.print(f"🤝 Top Counterparty: {top_addr} ({top_cnt} tx)")

    display_table(txs, args.limit)

    if not args.no_gas_graph:
        plot_gas_usage(txs)
    if not args.no_pie:
        plot_top_interactions(txs)


if __name__ == "__main__":
    main()
