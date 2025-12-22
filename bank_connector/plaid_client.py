"""Plaid API client wrapper for sandbox operations."""

from typing import Dict, Any
import plaid
from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products

from .config import Config


class PlaidClientWrapper:
    """Wrapper around Plaid API client for simplified sandbox operations.

    Handles API client initialization and provides methods for creating
    sandbox access tokens programmatically (without Link UI).
    """

    def __init__(self, config: Config):
        """Initialize Plaid API client with credentials from config.

        Args:
            config: Configuration object with Plaid credentials.
        """
        self.config = config

        # Configure Plaid API client
        configuration = plaid.Configuration(
            host=config.get_plaid_environment(),
            api_key={
                'clientId': config.PLAID_CLIENT_ID,
                'secret': config.PLAID_SECRET,
            }
        )

        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def create_sandbox_access_token(self, institution_id: str = 'ins_109508') -> str:
        """Create a sandbox access token programmatically.

        This bypasses the Plaid Link UI by using sandbox-specific endpoints
        to create a public token and exchange it for an access token.

        Args:
            institution_id: Plaid institution ID. Defaults to 'ins_109508'
                           (First Platypus Bank - a test institution).

        Returns:
            str: Access token for making API requests.

        Raises:
            plaid.ApiException: If API request fails.
        """
        # Step 1: Create a sandbox public token
        request = SandboxPublicTokenCreateRequest(
            institution_id=institution_id,
            initial_products=[Products('transactions')]
        )
        response = self.client.sandbox_public_token_create(request)
        public_token = response['public_token']

        # Step 2: Exchange public token for access token
        return self.exchange_public_token(public_token)

    def exchange_public_token(self, public_token: str) -> str:
        """Exchange a public token for an access token.

        Args:
            public_token: The public token to exchange.

        Returns:
            str: The access token.

        Raises:
            plaid.ApiException: If exchange fails.
        """
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        exchange_response = self.client.item_public_token_exchange(exchange_request)
        return exchange_response['access_token']

    def test_connection(self, access_token: str) -> Dict[str, Any]:
        """Test API connection by fetching item information.

        Args:
            access_token: The access token to test.

        Returns:
            Dict containing item information if successful.

        Raises:
            plaid.ApiException: If connection test fails.
        """
        from plaid.model.item_get_request import ItemGetRequest

        request = ItemGetRequest(access_token=access_token)
        response = self.client.item_get(request)
        return response.to_dict()
