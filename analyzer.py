# analyzer.py
# This script fetches and analyzes Ethereum transaction data from Etherscan

import requests
from tabulate import tabulate
from config import ETHERSCAN_API_KEY

ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"

def fetch_transactions(address):
    """Fetches transaction history for a given Ethereum address from Etherscan."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }

    response = requests.get(ETHERSCAN_BASE_URL, params=params)
    data = response.json()

    if data["status"] != "1":
        print("❌ Failed to fetch transactions:", data["message"])
        return []

    return data["result"]

def analyze_transactions(transactions):
    """Analyzes the total and average gas usage and the most interacted address."""
    total_gas = 0
    interaction_count = {}

    for tx in transactions:
        gas = int(tx["gasUsed"])
        to = tx["to"]

        total_gas += gas
        if to:
            interaction_count[to] = interaction_count.get(to, 0) + 1

    avg_gas = total_gas / len(transactions) if transactions else 0
    top_contact = max(interaction_count, key=interaction_count.get) if interaction_count else "N/A"

    print(f"📊 Total Transactions: {len(transactions)}")
    print(f"⛽️ Average Gas Used: {avg_gas:,.2f}")
    print(f"🤝 Most Interacted Address: {top_contact} ({interaction_count.get(top_contact, 0)} times)")

def display_table(transactions):
    """Displays a table of the first 10 transactions."""
    table_data = []
    for tx in transactions[:10]:
        table_data.append([
            tx["hash"][:10] + "...",
            tx["from"][:10] + "...",
            tx["to"][:10] + "...",
            int(tx["gasUsed"]),
            tx["timeStamp"]
        ])

    headers = ["TxHash", "From", "To", "GasUsed", "Timestamp"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    address = input("🧾 Enter Ethereum address: ").strip()
    transactions = fetch_transactions(address)
    if transactions:
        analyze_transactions(transactions)
        display_table(transactions)
