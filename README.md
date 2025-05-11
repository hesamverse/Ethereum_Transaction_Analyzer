# 🛠️ Ethereum Transaction Analyzer (ETA)

![PyPI](https://img.shields.io/pypi/v/eth-tx-analyzer?logo=pypi&label=PyPI)
![CI](https://img.shields.io/github/actions/workflow/status/hesamverse/eth-tx-analyzer/ci.yml?label=CI)
![License](https://img.shields.io/badge/license-MIT-yellow)
![pre‑commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)

A minimal CLI 🖥️ & TUI 🔮 toolkit that fetches, analyzes, and visualizes the full
transaction history of any Ethereum address—perfect for auditors, analysts, and curious builders.

---

## 📑 Table of Contents
1. [Key Features](#key-features)  
2. [Installation](#installation)  
3. [Quick Start](#quick-start)  
4. [Command Reference](#command-reference)  
5. [Examples](#examples)  
6. [Project Structure](#project-structure)  
7. [Roadmap](#roadmap)  
8. [Contributing](#contributing)  
9. [License & Credits](#license--credits)

---

## ✨ Key Features
| Category | What you get | CLI Flag / TUI Toggle |
|----------|--------------|-----------------------|
| **Rich tables** | ANSI‑styled overview of the latest *N* transactions | `--limit N` |
| **Gas analysis** | Average/total gas + interactive line‑chart | `--no-gas-graph` |
| **Counterparty insight** | Top‑N addresses + pie‑chart | `--no-pie`, `--top N` |
| **Multi‑chain ready** | Etherscan‑compatible APIs (ETH, BSC, Polygon…) | `--network polygon` |
| **Exports** | CSV / JSON / Parquet for downstream tooling | `--export csv` |
| **Caching** | `requests‑cache` to spare rate‑limits | automatic |
| **TUI** | Textual‑powered UI with mouse support | `etha-ui` |
| **Docker** | Zero‑dep container for CI/CD pipelines | `docker run …` |
| **Typed API** | `pydantic` models so you can `import eta` as a library | `from eta import Analyzer` |

---

## ⚡ Installation

<details>
<summary><b>pipx (recommended)</b></summary>

```bash
pipx install eth-tx-analyzer
```

</details>

<details>
<summary><b>Poetry (dev mode)</b></summary>

```bash
git clone https://github.com/hesamverse/eth-tx-analyzer.git
cd eth-tx-analyzer
poetry install --with dev
poetry run etha 0xABCD…
```

</details>

<details>
<summary><b>Docker</b></summary>

```bash
docker pull ghcr.io/hesamverse/eth-tx-analyzer:latest
docker run -it --rm ghcr.io/hesamverse/eth-tx-analyzer 0xABCD…
```

</details>

Requirement: a free Etherscan API key.  
Create `.env` in `~/.config/eta/` or export `ETHERSCAN_API_KEY`.

---

## 🚀 Quick Start

```bash
# Analyze the last 20 transactions of Vitalik’s address
etha 0xd8dA6BF… --limit 20

# Same address but with the Textual TUI
etha-ui
```

---

## 🛎️ Command Reference

```
Usage: etha [OPTIONS] ADDRESS

Options:
  --limit INTEGER           Number of recent txs to list        [default: 10]
  --network TEXT            eth | bsc | polygon | arbitrum
  --top INTEGER             Top‑N counterparties for pie‑chart  [default: 5]
  --no-gas-graph            Disable gas usage chart
  --no-pie                  Disable counterparty pie‑chart
  --export [csv|json|parquet]
  --verbose / --no-verbose  Toggle debug logging
  --help                    Show this message and exit.
```

---

## 🧩 Examples

| Task | Command |
|------|---------|
| Export all transactions to CSV | `etha 0xABCD… --limit 0 --export csv` |
| Headless mode (no charts) | `etha 0xABCD… --no-gas-graph --no-pie` |
| Analyze a Polygon wallet | `etha 0xABCD… --network polygon` |
| Use within Python | See `examples/notebook.ipynb` |

---

## 📂 Project Structure

```
ethereum_transaction_analyzer/
 ├─ eta/                  # package
 │   ├─ analyzer.py       # CLI
 │   ├─ interface.py      # TUI
 │   ├─ utils.py          # helpers
 │   ├─ config.py         # env loader
 │   └─ models.py         # pydantic Tx model
 ├─ tests/                # pytest
 ├─ docs/
 ├─ pyproject.toml
 ├─ README.md
 └─ LICENSE
```

---

## 🛣️ Roadmap

- Integrate `textual.widgets.DataTable` for scrollable tables  
- Automatic back‑off on Etherscan rate‑limits  
- Wallet‑level P&L cost‑basis analysis  
- StarkNet & Solana adapters  
- Publish to PyPI as `eth‑tx‑analyzer`

---

## 🤝 Contributing

Fork the repo & create your branch.

```bash
poetry install --with dev
pre-commit install
pytest -q
```

Then open a PR—clean diffs are loved here!

---

## 📜 License & Credits

MIT © 2025 [Hesameddin Jan‑Nesari Ladan](https://github.com/hesamverse)

Charts powered by Matplotlib; tables by Rich; TUI by Textual.  
Ethereum data courtesy of Etherscan.io.  
Built with ☕ + 💻 in Isfahan & Doha.
