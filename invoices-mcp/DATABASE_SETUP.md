# Database Setup for Invoices MCP Server

## Prerequisites

1. Install the required dependencies:
   ```bash
   cd invoices-mcp
   uv sync  # or pip install -e .
   ```

2. Set up a PostgreSQL database with the transactions table.

## Environment Configuration

Create a `.env` file in the `invoices-mcp` directory with the following variables:

```env
# OpenAI API Key for invoice processing
OPENAI_API_KEY=your_openai_api_key_here

# Mistral API Key for OCR processing
MISTRAL_API_KEY=your_mistral_api_key_here

# Database connection URL for PostgreSQL
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
```

## Database Schema

The transactions table should have the following structure in the `ivy_date` schema:

```sql
CREATE SCHEMA IF NOT EXISTS ivy_date;

CREATE TABLE ivy_date.transactions (
    transaction_id VARCHAR PRIMARY KEY,
    date DATE,
    amount NUMERIC,
    description TEXT,
    reference VARCHAR,
    category VARCHAR,
    currency VARCHAR,
    counterparty VARCHAR,
    provider VARCHAR,
    transaction_type VARCHAR,
    month_year VARCHAR,
    is_stripe_invoice BOOLEAN,
    is_invalid BOOLEAN,
    created_at TIMESTAMP WITHOUT TIME ZONE
);
```

**Note**: The table must be in the `ivy_date` schema, not the default `public` schema.

## Available MCP Tools

Once configured, the MCP server provides the following tools for querying transactions:

### 1. `get_transactions`
- **Description**: Get transactions with optional filtering
- **Returns**: Object containing `transactions` array and `count`
- **Parameters**:
  - `limit` (int, default=100): Maximum number of transactions to return
  - `category` (str, optional): Filter by transaction category
  - `provider` (str, optional): Filter by provider
  - `transaction_type` (str, optional): Filter by transaction type
  - `currency` (str, optional): Filter by currency
  - `counterparty` (str, optional): Filter by counterparty
  - `start_date` (date, optional): Start date filter (YYYY-MM-DD)
  - `end_date` (date, optional): End date filter (YYYY-MM-DD)
  - `is_stripe_invoice` (bool, optional): Filter by Stripe invoice status
  - `is_invalid` (bool, optional): Filter by validity status

### 2. `get_transaction_by_id`
- **Description**: Get a specific transaction by its ID
- **Returns**: Single transaction object
- **Parameters**:
  - `transaction_id` (str): The unique transaction ID

### 3. `search_transactions`
- **Description**: Search transactions by description or counterparty name
- **Returns**: Object containing `transactions` array and `count`
- **Parameters**:
  - `search_term` (str): Search term to match against description or counterparty
  - `limit` (int, default=50): Maximum number of transactions to return

### 4. `get_transaction_summary`
- **Description**: Get summary statistics about transactions
- **Returns**: Object with summary statistics including totals, breakdowns, and date ranges
- **Parameters**:
  - `category` (str, optional): Filter by transaction category
  - `provider` (str, optional): Filter by provider
  - `start_date` (date, optional): Start date filter (YYYY-MM-DD)
  - `end_date` (date, optional): End date filter (YYYY-MM-DD)

### 5. `find_and_download_invoice` (existing)
- **Description**: Find and download invoices from websites in a unified format

## Running the Server

1. Ensure your database is running and accessible
2. Set up your `.env` file with the correct database URL
3. Run the MCP server:
   ```bash
   python src/server.py
   ```

The server will start on port 8001 and provide both invoice downloading and transaction querying capabilities.

## Error Handling

- If the `DATABASE_URL` environment variable is not set, the database-related tools will raise a clear error message
- The server will still function for invoice downloading even if the database is not configured
- Database connection errors will be properly handled and reported 