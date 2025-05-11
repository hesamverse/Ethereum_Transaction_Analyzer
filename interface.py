# interface.py

from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static, Checkbox
from textual.containers import Vertical
from rich.table import Table
from config import ETHERSCAN_API_KEY
from utils import fetch_transactions, convert_timestamp
from utils import plot_gas_usage, plot_top_interactions

class AnalyzerApp(App):
    CSS_PATH = None  # We keep it simple
    TITLE = "Ethereum Transaction Analyzer"

    def compose(self) -> ComposeResult:
        yield Static("🔍 Enter Ethereum Address:", id="label")
        yield Input(placeholder="0x...", id="address_input")
        yield Checkbox("Show Gas Usage Graph", id="gas_checkbox", value=True)
        yield Checkbox("Show Interaction Pie Chart", id="pie_checkbox", value=True)
        yield Button(label="Analyze", id="run_button")
        yield Static("", id="result_box")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        address = self.query_one("#address_input", Input).value.strip()
        show_gas = self.query_one("#gas_checkbox", Checkbox).value
        show_pie = self.query_one("#pie_checkbox", Checkbox).value
        output_box = self.query_one("#result_box", Static)

        if not address.startswith("0x"):
            output_box.update("❌ Invalid address.")
            return

        output_box.update("⏳ Fetching transactions...")

        try:
            txs = fetch_transactions(address)
            if not txs:
                output_box.update("❗ No transactions found.")
                return

            # Create a table
            table = Table(title="📄 Recent Transactions", show_lines=True)
            table.add_column("Hash", style="bold cyan")
            table.add_column("From", style="dim")
            table.add_column("To", style="dim")
            table.add_column("Gas", style="yellow", justify="right")
            table.add_column("Date", style="green")

            for tx in txs[:10]:
                table.add_row(
                    tx["hash"][:8] + "...",
                    tx["from"][:8] + "...",
                    tx["to"][:8] + "...",
                    f"{int(tx['gasUsed']):,}",
                    convert_timestamp(tx["timeStamp"])
                )

            output_box.update(table)

            # Display graphs
            if show_gas:
                plot_gas_usage(txs)
            if show_pie:
                plot_top_interactions(txs)

        except Exception as e:
            output_box.update(f"🚨 Error: {e}")

if __name__ == "__main__":
    AnalyzerApp().run()
