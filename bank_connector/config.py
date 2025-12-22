"""Configuration management for Plaid Bank Connector."""

import os
from typing import Optional
from dotenv import load_dotenv
import plaid


class Config:
    """Manages configuration and credentials for Plaid API connection.

    Loads credentials from environment variables and validates their presence.
    Maps environment names to Plaid SDK environment objects.
    """

    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()

        self.PLAID_CLIENT_ID: Optional[str] = os.getenv('PLAID_CLIENT_ID')
        self.PLAID_SECRET: Optional[str] = os.getenv('PLAID_SECRET')
        self.PLAID_ENV: str = os.getenv('PLAID_ENV', 'sandbox')
        self.PLAID_ACCESS_TOKEN: Optional[str] = os.getenv('PLAID_ACCESS_TOKEN')

        self.validate()

    def validate(self) -> None:
        """Validate that required credentials are present.

        Raises:
            ValueError: If required credentials are missing.
        """
        if not self.PLAID_CLIENT_ID:
            raise ValueError(
                "Missing PLAID_CLIENT_ID in .env file. "
                "Get credentials from https://dashboard.plaid.com/"
            )

        if not self.PLAID_SECRET:
            raise ValueError(
                "Missing PLAID_SECRET in .env file. "
                "Get credentials from https://dashboard.plaid.com/"
            )

        if self.PLAID_ENV not in ['sandbox', 'development', 'production']:
            raise ValueError(
                f"Invalid PLAID_ENV: {self.PLAID_ENV}. "
                "Must be 'sandbox', 'development', or 'production'"
            )

    def get_plaid_environment(self) -> str:
        """Get the Plaid SDK environment URL based on configuration.

        Returns:
            str: The environment URL for Plaid API client.
        """
        env_map = {
            'sandbox': 'https://sandbox.plaid.com',
            'development': 'https://development.plaid.com',
            'production': 'https://production.plaid.com'
        }
        return env_map[self.PLAID_ENV.lower()]
