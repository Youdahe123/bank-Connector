"""CLI interface for Plaid Bank Connector."""

import sys
import click
from plaid.exceptions import ApiException

from .config import Config
from .plaid_client import PlaidClientWrapper
from .transaction_fetcher import TransactionFetcher
from .formatters import TransactionFormatter


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Plaid Bank Transaction CLI Tool.

    A simple command-line tool to fetch and display bank transaction
    data from Plaid's Sandbox environment.
    """
    pass


@cli.command()
@click.option(
    '--institution-id',
    default='ins_109508',
    help='Plaid institution ID (default: ins_109508 - First Platypus Bank)'
)
def setup(institution_id):
    """Setup Plaid sandbox connection and create access token.

    This command creates a sandbox access token that can be used to
    fetch transactions. The token should be added to your .env file.
    """
    try:
        click.echo("🔧 Setting up Plaid sandbox connection...")

        config = Config()
        plaid_client = PlaidClientWrapper(config)

        click.echo(f"Creating access token for institution: {institution_id}")
        access_token = plaid_client.create_sandbox_access_token(institution_id)

        click.echo()
        click.echo("✅ Successfully created sandbox access token!")
        click.echo()
        click.echo("Add this line to your .env file:")
        click.echo(f"PLAID_ACCESS_TOKEN={access_token}")
        click.echo()
        click.echo("Then run: python -m bank_connector.cli fetch-transactions")

    except ValueError as e:
        click.echo(f"❌ Configuration error: {str(e)}", err=True)
        click.echo("💡 Make sure you have a .env file with PLAID_CLIENT_ID and PLAID_SECRET", err=True)
        sys.exit(1)
    except ApiException as e:
        click.echo(f"❌ Plaid API error: {e}", err=True)
        click.echo("💡 Check your credentials at https://dashboard.plaid.com/", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def test_connection():
    """Test Plaid API connection and credentials.

    Verifies that your Plaid credentials are valid and you can
    connect to the API successfully.
    """
    try:
        click.echo("🔍 Testing Plaid API connection...")

        config = Config()

        if not config.PLAID_ACCESS_TOKEN:
            click.echo("❌ No access token found.", err=True)
            click.echo("💡 Run 'setup' command first to create an access token", err=True)
            sys.exit(1)

        plaid_client = PlaidClientWrapper(config)
        item_info = plaid_client.test_connection(config.PLAID_ACCESS_TOKEN)

        click.echo("✅ Connection successful!")
        click.echo()
        click.echo(f"Institution ID: {item_info['item']['institution_id']}")
        click.echo(f"Item ID: {item_info['item']['item_id']}")
        click.echo(f"Available products: {', '.join(item_info['item']['available_products'])}")

    except ValueError as e:
        click.echo(f"❌ Configuration error: {str(e)}", err=True)
        sys.exit(1)
    except ApiException as e:
        click.echo(f"❌ Plaid API error: {e}", err=True)
        click.echo("💡 Your access token may be invalid. Try running 'setup' again.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    '--days',
    default=30,
    type=int,
    help='Number of days to fetch (default: 30)'
)
@click.option(
    '--format',
    'output_format',
    type=click.Choice(['table', 'json', 'list'], case_sensitive=False),
    default='table',
    help='Output format (default: table)'
)
def fetch_transactions(days, output_format):
    """Fetch and display bank transactions.

    Retrieves transaction history for the specified number of days
    and displays it in the chosen format.
    """
    try:
        click.echo(f"Fetching transactions for the last {days} days...")
        click.echo()

        # Load configuration
        config = Config()

        if not config.PLAID_ACCESS_TOKEN:
            click.echo("❌ No access token found.", err=True)
            click.echo("💡 Run 'setup' command first to create an access token", err=True)
            sys.exit(1)

        # Initialize Plaid client and fetcher
        plaid_client = PlaidClientWrapper(config)
        fetcher = TransactionFetcher(plaid_client)

        # Fetch transactions
        transactions = fetcher.get_recent_transactions(config.PLAID_ACCESS_TOKEN, days)

        # Format and display output
        formatter = TransactionFormatter()

        if output_format == 'table':
            formatter.format_table(transactions)
        elif output_format == 'list':
            formatter.format_list(transactions)
        elif output_format == 'json':
            json_output = formatter.format_json(transactions)
            click.echo(json_output)

        if not transactions:
            click.echo()
            click.echo("💡 No transactions found in the specified date range.")

    except ValueError as e:
        click.echo(f"❌ Configuration error: {str(e)}", err=True)
        sys.exit(1)
    except ApiException as e:
        click.echo(f"❌ Plaid API error: {e}", err=True)
        click.echo("💡 Your access token may be invalid. Try running 'setup' again.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    cli()
