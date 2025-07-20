# Invoices MCP Server

A Model Context Protocol (MCP) server that provides unified invoice downloading and transaction querying capabilities.

## Features

### 🧾 Invoice Downloading
- Automatically find and download invoices from merchant websites
- Extract invoice content using OCR (Mistral API)
- Unified format for invoice data extraction

### 🔍 Transaction Querying
- Query transactions from a PostgreSQL database using SQLAlchemy
- Advanced filtering and search capabilities
- Summary statistics and analytics
- Full-text search across descriptions and counterparties

## Installation

1. Clone and navigate to the project directory:
   ```bash
   cd invoices-mcp
   ```

2. Install dependencies:
   ```bash
   uv sync
   # or
   pip install -e .
   ```

## Configuration

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed setup instructions.

### Quick Setup

1. Create a `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```

2. Set up your PostgreSQL database with the transactions table schema in the `ivy_date` schema (see DATABASE_SETUP.md)

**Important**: The transactions table must be in the `ivy_date` schema, not the default `public` schema.

## Usage

Start the MCP server:
```bash
python src/server.py
```

The server will run on port 8001 and provide the following tools:

## Available MCP Tools

### Invoice Tools
- **`find_and_download_invoice`** - Download and extract invoice data from merchant websites

### Transaction Tools
- **`get_transactions`** - Query transactions with filtering options
- **`get_transaction_by_id`** - Get a specific transaction by ID
- **`search_transactions`** - Full-text search across transaction descriptions
- **`get_transaction_summary`** - Get summary statistics and analytics

## Architecture

- **FastMCP**: MCP server framework
- **SQLAlchemy**: Database ORM for transaction queries
- **Browser-use**: Web automation for invoice downloading
- **Mistral OCR**: Invoice content extraction
- **PostgreSQL**: Transaction data storage

## Error Handling

- Graceful degradation: Invoice downloading works even if database is not configured
- Clear error messages for missing configuration
- Proper session management and cleanup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

See project license file.
