"""Output formatting utilities for transaction display."""

import json
from typing import List

from rich.console import Console
from rich.table import Table

from .transaction_fetcher import Transaction


class TransactionFormatter:
    """Formats transaction data for terminal display.

    Supports multiple output formats including formatted tables,
    simple lists, and JSON output.
    """

    def __init__(self):
        """Initialize the formatter with a Rich console."""
        self.console = Console()

    def format_table(self, transactions: List[Transaction]) -> None:
        """Display transactions as a formatted table.

        Args:
            transactions: List of transactions to display.
        """
        if not transactions:
            self.console.print("[yellow]No transactions found.[/yellow]")
            return

        # Create table with columns (no fixed widths for better adaptability)
        table = Table(title="Bank Transactions", show_header=True, header_style="bold magenta")
        table.add_column("Date", style="cyan", no_wrap=True)
        table.add_column("Amount", justify="right", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Merchant", style="blue")
        table.add_column("Category", style="green")
        table.add_column("Status", no_wrap=True)

        # Add rows
        total_debits = 0.0
        total_credits = 0.0

        for txn in transactions:
            # Color code amounts (Plaid uses positive for debits, negative for credits)
            if txn.amount > 0:
                amount_str = f"[red]-${txn.amount:.2f}[/red]"
                total_debits += txn.amount
            else:
                amount_str = f"[green]+${abs(txn.amount):.2f}[/green]"
                total_credits += abs(txn.amount)

            # Format merchant name
            merchant = txn.merchant_name or "N/A"

            # Format category (show first 2 categories)
            category = ", ".join(txn.category[:2]) if txn.category else "Uncategorized"

            # Format status
            status = "[yellow]Pending[/yellow]" if txn.pending else "[green]Posted[/green]"

            table.add_row(
                txn.date,
                amount_str,
                txn.description,
                merchant,
                category,
                status
            )

        # Display table
        self.console.print(table)

        # Display summary
        self.console.print()
        self.console.print(f"[bold]Summary:[/bold]")
        self.console.print(f"  Total Debits:  [red]-${total_debits:.2f}[/red]")
        self.console.print(f"  Total Credits: [green]+${total_credits:.2f}[/green]")
        self.console.print(f"  Net Change:    ${(total_credits - total_debits):.2f}")
        self.console.print(f"  Transactions:  {len(transactions)}")

    def format_list(self, transactions: List[Transaction]) -> None:
        """Display transactions as a simple list.

        Args:
            transactions: List of transactions to display.
        """
        if not transactions:
            self.console.print("[yellow]No transactions found.[/yellow]")
            return

        for i, txn in enumerate(transactions, 1):
            # Color code amount
            if txn.amount > 0:
                amount_str = f"[red]-${txn.amount:.2f}[/red]"
            else:
                amount_str = f"[green]+${abs(txn.amount):.2f}[/green]"

            status = "[yellow](Pending)[/yellow]" if txn.pending else ""

            self.console.print(f"{i}. {txn.date} | {amount_str} | {txn.description} {status}")
            if txn.merchant_name:
                self.console.print(f"   Merchant: {txn.merchant_name}")
            if txn.category:
                self.console.print(f"   Category: {', '.join(txn.category)}")
            self.console.print()

    def format_json(self, transactions: List[Transaction]) -> str:
        """Format transactions as JSON.

        Args:
            transactions: List of transactions to format.

        Returns:
            JSON string representation of transactions.
        """
        transactions_dict = [
            {
                'transaction_id': txn.transaction_id,
                'date': txn.date,
                'amount': txn.amount,
                'description': txn.description,
                'merchant_name': txn.merchant_name,
                'category': txn.category,
                'pending': txn.pending
            }
            for txn in transactions
        ]
        return json.dumps(transactions_dict, indent=2)
