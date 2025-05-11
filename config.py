#!/usr/bin/env python3
"""Load configuration for Ethereum Transaction Analyzer."""

import os
from dotenv import load_dotenv

load_dotenv()  # Reads .env if present

ETHERSCAN_API_KEY: str | None = os.getenv("ETHERSCAN_API_KEY")

if ETHERSCAN_API_KEY is None:
    raise EnvironmentError(
        "❌ ETHERSCAN_API_KEY not found. Add it to .env or env variables."
    )
