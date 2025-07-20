import asyncio
import base64
import datetime
import logging
import os
from typing import Annotated, Optional

from agent import Result, create_agent
from dotenv import load_dotenv
from fastmcp import FastMCP
from mistralai import Mistral
from mistralai.extra import response_format_from_pydantic_model
from models import (
    Transaction,
    TransactionListResponse,
    TransactionResponse,
    TransactionSummaryResponse,
    get_database_manager,
)
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

logger = logging.getLogger(__name__)


class ExtractedInvoiceContent(BaseModel):
    invoice_date: str = Field(
        description="The date of the invoice, in the format YYYY-MM-DD",
    )
    invoice_amount: float = Field(description="The amount of the invoice")
    invoice_number: str = Field(description="The number of the invoice")
    invoice_currency: str = Field(description="The currency of the invoice")


class ExtractedInvoiceWithData(ExtractedInvoiceContent):
    invoice_file_path: str = Field(description="The path to the invoice file")


def encode_pdf(pdf_path):
    """Encode the pdf to base64."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None


openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

mistral = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Initialize database manager
try:
    db_manager = get_database_manager()
except ValueError as e:
    logger.warning(f"Database not configured: {e}")
    db_manager = None


def transaction_to_response(transaction: Transaction) -> TransactionResponse:
    """Convert a SQLAlchemy Transaction object to a TransactionResponse Pydantic model."""
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        date=transaction.date.isoformat() if transaction.date else None,
        amount=float(transaction.amount) if transaction.amount else None,
        description=transaction.description,
        reference=transaction.reference,
        category=transaction.category,
        currency=transaction.currency,
        counterparty=transaction.counterparty,
        provider=transaction.provider,
        transaction_type=transaction.transaction_type,
        month_year=transaction.month_year,
        is_stripe_invoice=transaction.is_stripe_invoice,
        is_invalid=transaction.is_invalid,
        created_at=transaction.created_at.isoformat()
        if transaction.created_at
        else None,
    )


mcp = FastMCP(
    name="Unified Invoices Downloader",
    instructions="""
    This MCP server is used to download invoices from websites in a unified format and query transactions from the database.
    """,
    port=8001,
)


@mcp.tool(
    name="find_and_download_invoice",
    description="Find and download invoices from websites in a unified format.",
    output_schema=ExtractedInvoiceWithData.model_json_schema(),
)
async def find_and_download_invoice(
    domainOrUrl: Annotated[
        str,
        Field(
            description="The domain or url of the merchant or website that issued the invoice, e.g. 'example.com' without the 'https://' prefix",
            pattern=r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$",
        ),
    ],
    date: Annotated[
        datetime.date,
        Field(description="The date of the transaction, in the format YYYY-MM-DD"),
    ],
    reference: Annotated[
        str,
        Field(description="The reference of the transaction, e.g. a transaction ID"),
    ],
    amount: Annotated[
        float,
        Field(
            description="The amount of the transaction, in the currency of the invoice"
        ),
    ],
) -> ExtractedInvoiceWithData:
    agent = await create_agent(
        domainOrUrl=domainOrUrl,
        tx_date=date,
        tx_amount=amount,
        tx_reference=reference,
    )
    history = await agent.run()

    result = history.final_result()

    if result:
        parsed: Result = Result.model_validate_json(result)
        if parsed.downloaded_file_path and len(parsed.downloaded_file_path) > 0:
            pdf_file_path = parsed.downloaded_file_path
        else:
            raise ValueError("No invoice found by agent")
    else:
        raise ValueError("No invoice result found in agent history")

    logger.info(f"Got Invoice PDF file path: {pdf_file_path}")

    # Extract text from PDF
    pdf_encoded = encode_pdf(pdf_file_path)

    logger.info("Got PDF encoded")

    response = await mistral.ocr.process_async(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{pdf_encoded}",
        },
        document_annotation_format=response_format_from_pydantic_model(
            ExtractedInvoiceContent
        ),
        include_image_base64=True,
        timeout_ms=30000,
    )

    logger.info(f"Got Mistral OCR response: {response.document_annotation}")

    if response.document_annotation:
        content = ExtractedInvoiceContent.model_validate_json(
            response.document_annotation
        )
    else:
        raise ValueError("No invoice content found in Mistral OCR response")

    return ExtractedInvoiceWithData(
        invoice_file_path=pdf_file_path,
        **content.model_dump(),
    )


@mcp.tool(
    name="get_transactions",
    description="Get transactions from the database",
    output_schema=TransactionListResponse.model_json_schema(),
)
async def get_transactions(
    limit: Annotated[
        int, Field(description="Maximum number of transactions to return", default=100)
    ] = 100,
) -> TransactionListResponse:
    if not db_manager:
        raise ValueError(
            "Database not configured. Please set DATABASE_URL environment variable."
        )

    session = db_manager.get_session()
    try:
        query = session.query(Transaction)

        # Order by date descending and apply limit
        query = query.order_by(Transaction.date.desc()).limit(limit)

        transactions = query.all()
        transaction_responses = [transaction_to_response(t) for t in transactions]

        return TransactionListResponse(
            transactions=transaction_responses, count=len(transaction_responses)
        )
    finally:
        session.close()


# @mcp.tool(
#     name="get_transaction_by_id",
#     description="Get a specific transaction by its ID",
#     output_schema=TransactionResponse.model_json_schema(),
# )
# async def get_transaction_by_id(
#     transaction_id: Annotated[str, Field(description="The unique transaction ID")],
# ) -> TransactionResponse:
#     if not db_manager:
#         raise ValueError(
#             "Database not configured. Please set DATABASE_URL environment variable."
#         )

#     session = db_manager.get_session()
#     try:
#         transaction = (
#             session.query(Transaction)
#             .filter(Transaction.transaction_id == transaction_id)
#             .first()
#         )

#         if not transaction:
#             raise ValueError(f"Transaction with ID {transaction_id} not found")

#         return transaction_to_response(transaction)
#     finally:
#         session.close()


# @mcp.tool(
#     name="search_transactions",
#     description="Search transactions by description or counterparty name",
#     output_schema=TransactionListResponse.model_json_schema(),
# )
# async def search_transactions(
#     search_term: Annotated[
#         str,
#         Field(description="Search term to match against description or counterparty"),
#     ],
#     limit: Annotated[
#         int, Field(description="Maximum number of transactions to return", default=50)
#     ] = 50,
# ) -> TransactionListResponse:
#     if not db_manager:
#         raise ValueError(
#             "Database not configured. Please set DATABASE_URL environment variable."
#         )

#     session = db_manager.get_session()
#     try:
#         query = (
#             session.query(Transaction)
#             .filter(
#                 or_(
#                     Transaction.description.ilike(f"%{search_term}%"),
#                     Transaction.counterparty.ilike(f"%{search_term}%"),
#                 )
#             )
#             .order_by(Transaction.date.desc())
#             .limit(limit)
#         )

#         transactions = query.all()
#         transaction_responses = [transaction_to_response(t) for t in transactions]

#         return TransactionListResponse(
#             transactions=transaction_responses, count=len(transaction_responses)
#         )
#     finally:
#         session.close()


@mcp.tool(
    name="get_transaction_summary",
    description="Get summary statistics about transactions",
    output_schema=TransactionSummaryResponse.model_json_schema(),
)
async def get_transaction_summary(
    category: Annotated[
        Optional[str], Field(description="Filter by transaction category")
    ] = None,
    provider: Annotated[Optional[str], Field(description="Filter by provider")] = None,
    start_date: Annotated[
        Optional[datetime.date], Field(description="Start date filter (YYYY-MM-DD)")
    ] = None,
    end_date: Annotated[
        Optional[datetime.date], Field(description="End date filter (YYYY-MM-DD)")
    ] = None,
) -> TransactionSummaryResponse:
    if not db_manager:
        raise ValueError(
            "Database not configured. Please set DATABASE_URL environment variable."
        )

    session = db_manager.get_session()
    try:
        query = session.query(Transaction).filter(Transaction.is_invalid != True)

        # Apply filters
        if category:
            query = query.filter(Transaction.category == category)
        if provider:
            query = query.filter(Transaction.provider == provider)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        transactions = query.all()

        # Calculate summary statistics
        total_count = len(transactions)
        total_amount = sum(float(t.amount) if t.amount else 0 for t in transactions)

        # Group by categories, providers, currencies
        categories = {}
        providers = {}
        currencies = {}
        dates = [t.date for t in transactions if t.date]

        for t in transactions:
            if t.category:
                categories[t.category] = categories.get(t.category, 0) + 1
            if t.provider:
                providers[t.provider] = providers.get(t.provider, 0) + 1
            if t.currency:
                currencies[t.currency] = currencies.get(t.currency, 0) + 1

        date_range = {}
        if dates:
            date_range = {
                "earliest": min(dates).isoformat(),
                "latest": max(dates).isoformat(),
            }

        return TransactionSummaryResponse(
            total_count=total_count,
            total_amount=total_amount,
            categories=categories,
            providers=providers,
            currencies=currencies,
            date_range=date_range,
        )
    finally:
        session.close()


async def main():
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())
