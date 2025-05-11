# config.py
# This module loads environment variables and makes them accessible to the app

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Extract the API key from environment
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

if not ETHERSCAN_API_KEY:
    raise ValueError("❌ Etherscan API key not found. Please set it in the .env file.")