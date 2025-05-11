# utils.py
# Utility functions for Ethereum Transaction Analyzer

from datetime import datetime

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