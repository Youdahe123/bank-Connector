"""Transaction fetching and parsing logic."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from plaid.model.transactions_get_request import TransactionsGetRequest

from .plaid_client import PlaidClientWrapper


@dataclass
class Transaction:
    """Represents a single bank transaction.

    Attributes:
        transaction_id: Unique transaction identifier from Plaid.
        date: Transaction date in YYYY-MM-DD format.
        amount: Transaction amount (positive for debits, negative for credits).
        description: Transaction description/name.
        merchant_name: Name of the merchant (if available).
        category: List of category strings.
        pending: Whether the transaction is pending or posted.
    """
    transaction_id: str
    date: str
    amount: float
    description: str
    merchant_name: Optional[str]
    category: List[str]
    pending: bool


class TransactionFetcher:
    """Handles fetching and parsing transaction data from Plaid.

    Provides methods to retrieve transactions for a given date range
    and convert them from Plaid's format to our simplified Transaction model.
    """

    def __init__(self, plaid_client: PlaidClientWrapper):
        """Initialize the transaction fetcher.

        Args:
            plaid_client: Configured Plaid API client wrapper.
        """
        self.plaid_client = plaid_client

    def get_recent_transactions(
        self,
        access_token: str,
        days: int = 30
    ) -> List[Transaction]:
        """Fetch transactions from the last N days.

        Args:
            access_token: Plaid access token for the account.
            days: Number of days to look back (default: 30).

        Returns:
            List of Transaction objects, sorted by date (newest first).

        Raises:
            plaid.ApiException: If API request fails.
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        return self.fetch_transactions(
            access_token,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )

    def fetch_transactions(
        self,
        access_token: str,
        start_date: str,
        end_date: str
    ) -> List[Transaction]:
        """Fetch transactions for a specific date range.

        Args:
            access_token: Plaid access token for the account.
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.

        Returns:
            List of Transaction objects, sorted by date (newest first).

        Raises:
            plaid.ApiException: If API request fails.
        """
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date()
        )

        response = self.plaid_client.client.transactions_get(request)
        transactions = response['transactions']

        # Parse and sort transactions
        parsed_transactions = [self._parse_transaction(t) for t in transactions]
        return sorted(parsed_transactions, key=lambda x: x.date, reverse=True)

    def _parse_transaction(self, raw_transaction: dict) -> Transaction:
        """Convert a Plaid transaction to our Transaction model.

        Args:
            raw_transaction: Raw transaction dict from Plaid API.

        Returns:
            Transaction object with extracted fields.
        """
        # Convert date object to string if needed
        date_value = raw_transaction['date']
        if hasattr(date_value, 'strftime'):
            date_str = date_value.strftime('%Y-%m-%d')
        else:
            date_str = str(date_value)

        return Transaction(
            transaction_id=raw_transaction['transaction_id'],
            date=date_str,
            amount=raw_transaction['amount'],
            description=raw_transaction['name'],
            merchant_name=raw_transaction.get('merchant_name'),
            category=raw_transaction.get('category', []),
            pending=raw_transaction['pending']
        )
