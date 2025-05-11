# 🚀 Ethereum Transaction Analyzer

A CLI and TUI (Text-based UI) tool to analyze Ethereum wallet activity — view transactions, calculate gas usage, detect most interacted addresses, and visualize data with clean charts.

---

## 📌 Features

- 🔍 Analyze any Ethereum address
- 📊 Table of recent transactions
- ⛽ Average and total gas usage
- 🤝 Identify most interacted addresses
- 📈 Visualize gas usage over time (Line Chart)
- 🥧 Visualize address interaction share (Pie Chart)
- 🎨 TUI with [Textual](https://github.com/Textualize/textual)
- 💻 Secure: loads Etherscan API key from `.env` file

---

## 🛠 Installation

```bash
git clone https://github.com/hesamverse/Ethereum-Transaction-Analyzer.git
cd Ethereum-Transaction-Analyzer
pip install -r requirements.txt

---

🔐 Setup .env
Create a .env file in the root directory:

ETHERSCAN_API_KEY=your_etherscan_api_key_here

Don't forget: .env is ignored by Git.

---

🚦 Usage
🧵 CLI mode:
python analyzer.py 0xYourAddressHere --limit 5 --no-gas-graph
--limit N → number of transactions to show

--no-gas-graph → disable gas graph

--no-pie → disable pie chart

---

🖥 TUI mode (Textual):
python interface.py
Graph toggle options included

Exit button and q shortcut to quit

Transaction table renders inside terminal

---

🧰 Dependencies
Python ≥ 3.7

requests, python-dotenv, rich, matplotlib, textual

---

📁 Project Structure
├── analyzer.py         # CLI analyzer
├── interface.py        # Textual-based UI
├── utils.py            # Reusable helper functions
├── config.py           # Loads Etherscan API key
├── requirements.txt    # Dependencies
├── .env                # Your local API key (not pushed)
└── LICENSE             # MIT License

---

📜 License
MIT © 2025 Hesameddin Jan-Nesari Ladan

---
🤝 Contribute
This is a solo-built personal project for resume, education, and fun.
Feel free to fork, suggest improvements, or reach out on GitHub or X (Twitter).