"""Bank Connector - Plaid Transaction CLI Tool.

A simple command-line tool to fetch and display bank transaction
data from Plaid's Sandbox environment.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .config import Config
from .plaid_client import PlaidClientWrapper
from .transaction_fetcher import TransactionFetcher, Transaction
from .formatters import TransactionFormatter

__all__ = [
    'Config',
    'PlaidClientWrapper',
    'TransactionFetcher',
    'Transaction',
    'TransactionFormatter',
]
