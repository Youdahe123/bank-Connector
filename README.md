# Bank Connector - Plaid Transaction CLI Tool

A simple Python command-line tool to fetch and display bank transaction data from Plaid's Sandbox environment. Perfect for testing Plaid integration, retrieving transaction history, and understanding how bank data flows through the Plaid API.

## Features

- Connect to Plaid Sandbox (test environment)
- Fetch transaction history (amount, date, description, merchant, category)
- Beautiful terminal table output with color-coded amounts
- Multiple output formats: table, list, and JSON
- Secure credential management via environment variables
- Built-in connection testing

## Prerequisites

- Python 3.8 or higher
- Plaid account (free developer account)
- pip (Python package manager)

## Installation

### 1. Clone or Download

```bash
cd /Users/asfawy/bankConnector
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `plaid-python` - Official Plaid Python SDK
- `python-dotenv` - Environment variable management
- `click` - CLI framework
- `rich` - Terminal formatting and tables

## Configuration

### 1. Get Plaid Credentials

1. Sign up for a free Plaid account at [https://dashboard.plaid.com/signup](https://dashboard.plaid.com/signup)
2. Verify your email address
3. Navigate to **Team Settings → Keys**
4. Copy your:
   - **client_id**
   - **sandbox secret** (starts with "sandbox-")

### 2. Create .env File

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
PLAID_CLIENT_ID=your_client_id_here
PLAID_SECRET=sandbox-your_secret_here
PLAID_ENV=sandbox
```

**Important:** Never commit your `.env` file to version control. It's already listed in `.gitignore`.

### 3. Create Access Token

Run the setup command to create a sandbox access token:

```bash
python -m bank_connector.cli setup
```

This will output an access token. Add it to your `.env` file:

```env
PLAID_ACCESS_TOKEN=access-sandbox-xxxxx
```

## Usage

### Fetch Transactions (Table Format)

Display the last 30 days of transactions in a formatted table:

```bash
python -m bank_connector.cli fetch-transactions
```

### Fetch Transactions (Custom Days)

Fetch transactions for a specific number of days:

```bash
python -m bank_connector.cli fetch-transactions --days 60
```

### JSON Output

Get transactions in JSON format for processing:

```bash
python -m bank_connector.cli fetch-transactions --format json
```

### List Format

Display transactions as a simple list:

```bash
python -m bank_connector.cli fetch-transactions --format list
```

### Test Connection

Verify your API credentials and connection:

```bash
python -m bank_connector.cli test-connection
```

## Commands

| Command | Description | Options |
|---------|-------------|---------|
| `setup` | Create sandbox access token | `--institution-id` (default: ins_109508) |
| `fetch-transactions` | Fetch and display transactions | `--days` (default: 30), `--format` (table/json/list) |
| `test-connection` | Test API credentials | None |

## Example Output

### Table Format

```
                                    Bank Transactions
┏━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Date       ┃     Amount ┃ Description                  ┃ Merchant           ┃ Category           ┃   Status ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 2024-01-15 │    -$45.23 │ Starbucks Coffee             │ Starbucks          │ Food and Drink     │   Posted │
│ 2024-01-14 │   +$500.00 │ Payroll Deposit              │ N/A                │ Transfer           │   Posted │
│ 2024-01-13 │    -$23.45 │ Amazon Purchase              │ Amazon             │ Shopping           │  Pending │
└────────────┴────────────┴──────────────────────────────┴────────────────────┴────────────────────┴──────────┘

Summary:
  Total Debits:  -$68.68
  Total Credits: +$500.00
  Net Change:    $431.32
  Transactions:  3
```

## Project Structure

```
bankConnector/
├── .env                          # Your credentials (gitignored)
├── .env.example                  # Template for .env
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── bank_connector/               # Main package
    ├── __init__.py              # Package initialization
    ├── cli.py                   # CLI commands
    ├── config.py                # Configuration management
    ├── plaid_client.py          # Plaid API wrapper
    ├── transaction_fetcher.py   # Transaction logic
    └── formatters.py            # Output formatting
```

## Plaid Sandbox

This tool uses Plaid's **Sandbox environment**, which provides:

- Free, unlimited API calls
- Fake/mock transaction data
- Test bank institutions
- All Plaid features for development
- No real bank connections
- Not for production use

### Default Test Institution

The tool uses **First Platypus Bank** (institution ID: `ins_109508`) by default, which provides sample transaction data for testing.

## Troubleshooting

### "Missing PLAID_CLIENT_ID in .env file"

**Solution:** Make sure you have created a `.env` file and added your credentials from the Plaid dashboard.

### "No access token found"

**Solution:** Run the `setup` command first:
```bash
python -m bank_connector.cli setup
```

### "Plaid API error: invalid_credentials"

**Solution:** Double-check your `PLAID_CLIENT_ID` and `PLAID_SECRET` in the `.env` file. Make sure you're using the **sandbox** secret (not development or production).

### "No transactions found"

**Solution:** Sandbox accounts have preset transaction data. If you see no transactions:
- The date range might be outside the available data
- Try running `test-connection` to verify your setup
- Try the default 30-day range

## Development

### Running Tests

(Tests not yet implemented - future enhancement)

### Making Changes

1. Activate virtual environment: `source venv/bin/activate`
2. Make your changes to the code
3. Test with: `python -m bank_connector.cli fetch-transactions`

## Future Enhancements

- Multiple bank account support
- Local database storage (SQLite)
- Transaction filtering and search
- CSV/Excel export
- Budget tracking features
- Support for real bank connections (beyond sandbox)
- Web dashboard interface

## Security Notes

- Never commit your `.env` file
- Never share your Plaid credentials
- Sandbox secrets are for testing only
- Use separate credentials for production

## Resources

- [Plaid API Documentation](https://plaid.com/docs/)
- [Plaid Dashboard](https://dashboard.plaid.com/)
- [Plaid Python SDK](https://github.com/plaid/plaid-python)
- [Plaid Sandbox Guide](https://plaid.com/docs/sandbox/)

## License

This is a personal project for learning and development purposes.

## Support

For Plaid-related questions, visit [Plaid Support](https://support.plaid.com/).

For issues with this tool, check the troubleshooting section above.
