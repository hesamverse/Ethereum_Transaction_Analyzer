# utils.py
# Utility functions for Ethereum Transaction Analyzer

from datetime import datetime
import matplotlib.pyplot as plt

def convert_timestamp(unix_timestamp):
    """
    Converts a UNIX timestamp (in seconds) to a human-readable datetime string.
    
    Args:
        unix_timestamp (str or int): The UNIX timestamp (seconds since epoch)
    
    Returns:
        str: Formatted date string in "YYYY-MM-DD HH:MM:SS" format
    """
    try:
        ts = int(unix_timestamp)
        return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return "Invalid Timestamp"
    
def plot_gas_usage(transactions):
    """
    Draws a line chart of gas used over time.
    """
    if not transactions:
        print("⚠️ No transactions to plot.")
        return

    dates = []
    gas_values = []

    for tx in transactions:
        try:
            date = convert_timestamp(tx["timeStamp"])[:10]  # فقط تاریخ (بدون ساعت)
            gas = int(tx["gasUsed"])
            dates.append(date)
            gas_values.append(gas)
        except Exception as e:
            print("⛔ Error in plotting:", e)

    plt.figure(figsize=(12, 5))
    plt.plot(dates, gas_values, marker='o')
    plt.xticks(rotation=45)
    plt.title("⛽ Gas Usage Over Time")
    plt.xlabel("Date")
    plt.ylabel("Gas Used")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def plot_top_interactions(transactions, top_n=5):
    """
    Plots a pie chart of the top N most interacted 'to' addresses.
    """
    from collections import Counter
    import matplotlib.pyplot as plt

    if not transactions:
        print("⚠️ No transactions to plot.")
        return

    interaction_counter = Counter()

    for tx in transactions:
        to_address = tx["to"]
        if to_address:
            interaction_counter[to_address] += 1

    # Get N most frequent addresses
    most_common = interaction_counter.most_common(top_n)
    labels = [item[0][:8] + "..." for item in most_common]
    counts = [item[1] for item in most_common]

    # Add "Other" category (lesser interactions)
    others_count = sum(interaction_counter.values()) - sum(counts)
    if others_count > 0:
        labels.append("Others")
        counts.append(others_count)

    # Draw a chart
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("🤝 Interaction Distribution")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()
