import os
from datetime import date as Date_Type
from datetime import datetime as DateTime_Type
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Numeric,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "ivy_data"}

    transaction_id: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[Optional[Date_Type]] = mapped_column(Date)
    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    description: Mapped[Optional[str]] = mapped_column(Text)
    reference: Mapped[Optional[str]] = mapped_column(String)
    category: Mapped[Optional[str]] = mapped_column(String)
    currency: Mapped[Optional[str]] = mapped_column(String)
    counterparty: Mapped[Optional[str]] = mapped_column(String)
    provider: Mapped[Optional[str]] = mapped_column(String)
    transaction_type: Mapped[Optional[str]] = mapped_column(String)
    month_year: Mapped[Optional[str]] = mapped_column(String)
    is_stripe_invoice: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_invalid: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[DateTime_Type]] = mapped_column(DateTime)


class TransactionResponse(BaseModel):
    transaction_id: str
    date: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    category: Optional[str] = None
    currency: Optional[str] = None
    counterparty: Optional[str] = None
    provider: Optional[str] = None
    transaction_type: Optional[str] = None
    month_year: Optional[str] = None
    is_stripe_invoice: Optional[bool] = None
    is_invalid: Optional[bool] = None
    created_at: Optional[str] = None


class TransactionListResponse(BaseModel):
    """Wrapper for list of transactions to comply with MCP spec requiring object outputs."""

    transactions: List[TransactionResponse]
    count: int


class TransactionSummaryResponse(BaseModel):
    """Response model for transaction summary statistics."""

    total_count: int
    total_amount: float
    categories: dict[str, int]
    providers: dict[str, int]
    currencies: dict[str, int]
    date_range: dict[str, str]


class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self):
        return self.SessionLocal()


# Initialize database manager with environment variable
def get_database_manager():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    return DatabaseManager(database_url)
