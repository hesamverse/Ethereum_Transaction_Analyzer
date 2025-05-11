#!/usr/bin/env python3
"""TUI (Textual) interface for Ethereum Transaction Analyzer."""

from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static, Checkbox, Footer, Header
from textual.containers import Horizontal
from textual.screen import Screen
from rich.table import Table

from utils import (
    fetch_transactions,
    convert_timestamp,
    plot_gas_usage,
    plot_top_interactions,
)


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("🔍 Ethereum Transaction Analyzer", id="title", classes="center")
        yield Input(placeholder="0x… Ethereum address", id="address_input")
        yield Input(placeholder="Limit (default 10)", id="limit_input")

        yield Horizontal(
            Checkbox("Gas Graph", id="gas_checkbox", value=True),
            Checkbox("Pie Chart", id="pie_checkbox", value=True),
            classes="center",
        )

        yield Horizontal(
            Button(label="Analyze", id="run_button", variant="success"),
            Button(label="Exit", id="exit_button", variant="error"),
            classes="center",
        )

        yield Static("", id="result_box")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit_button":
            await self.app.action_quit()
            return
        if event.button.id != "run_button":
            return

        addr = self.query_one("#address_input", Input).value.strip()
        limit_raw = self.query_one("#limit_input", Input).value.strip()
        limit = int(limit_raw) if limit_raw.isdigit() else 10

        show_gas = self.query_one("#gas_checkbox", Checkbox).value
        show_pie = self.query_one("#pie_checkbox", Checkbox).value
        result_box = self.query_one("#result_box", Static)

        if not (addr.startswith("0x") and len(addr) == 42):
            result_box.update("❌ Invalid Ethereum address.")
            return

        result_box.update("⏳ Fetching…")
        try:
            txs = fetch_transactions(addr)
        except Exception as exc:
            result_box.update(f"🚨 {exc}")
            return

        if not txs:
            result_box.update("🚫 No transactions found.")
            return

        table = Table(title=f"📄 Latest {limit} Transactions", show_lines=True)
        table.add_column("Hash", style="bold cyan")
        table.add_column("From", style="dim")
        table.add_column("To", style="dim")
        table.add_column("Gas", justify="right", style="yellow")
        table.add_column("Date", style="green")

        for tx in txs[:limit]:
            table.add_row(
                tx["hash"][:8] + "…",
                tx["from"][:8] + "…",
                tx["to"][:8] + "…",
                f"{int(tx['gasUsed']):,}",
                convert_timestamp(tx["timeStamp"]),
            )

        result_box.update(table)

        if show_gas:
            plot_gas_usage(txs)
        if show_pie:
            plot_top_interactions(txs)


class AnalyzerTUI(App):
    TITLE = "Ethereum Analyzer"
    CSS_PATH = None
    BINDINGS = [("q", "quit", "Quit")]

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    AnalyzerTUI().run()
