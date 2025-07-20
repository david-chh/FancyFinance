"""
LangChain tools to query your transaction database
AI-powered financial analysis using OpenAI + your data pipeline
"""

import os
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from typing import Type
from pydantic import BaseModel, Field
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.njyncmeeqjrtultxcpgb:xtz1KQD-btj8nzf5gtz@aws-0-eu-central-1.pooler.supabase.com:5432/postgres")

class TransactionQueryInput(BaseModel):
    query: str = Field(description="SQL query to execute on transaction data")

class TransactionQueryTool(BaseTool):
    name: str = "transaction_query"
    description: str = """Query financial transaction data directly with SQL. 
    Use this to answer specific questions about expenses, revenue, categories, dates, etc.
    Available tables: ivy_data.transactions, ivy_data.stripe_invoices
    Common columns: transaction_id, date, amount, description, category, counterparty, transaction_type, is_stripe_invoice"""
    args_schema: Type[BaseModel] = TransactionQueryInput
    
    def _run(self, query: str) -> str:
        """Execute database query and return results"""
        try:
            engine = create_engine(DATABASE_URL)
            df = pd.read_sql(query, engine)
            
            if df.empty:
                return "No results found for this query."
            
            # Format numbers nicely
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64'] and 'amount' in col.lower():
                    df[col] = df[col].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "N/A")
            
            return df.to_string(index=False, max_rows=20)
        except Exception as e:
            return f"Query error: {str(e)}"

class FinancialSummaryInput(BaseModel):
    period: str = Field(default="all", description="Time period for analysis: 'all', 'monthly', 'recent'")

class FinancialSummaryTool(BaseTool):
    name: str = "financial_summary"
    description: str = "Get comprehensive financial summary: total income, expenses, net profit, transaction counts"
    args_schema: Type[BaseModel] = FinancialSummaryInput
    
    def _run(self, period: str = "all") -> str:
        """Get financial analysis"""
        try:
            engine = create_engine(DATABASE_URL)
            
            # Overall summary
            summary_query = """
            SELECT 
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as total_expenses,
                SUM(amount) as net_result,
                COUNT(*) as total_transactions,
                COUNT(CASE WHEN is_stripe_invoice = true THEN 1 END) as stripe_invoices,
                COUNT(CASE WHEN is_invalid = true THEN 1 END) as invalid_transactions
            FROM ivy_data.transactions
            """
            
            df = pd.read_sql(summary_query, engine)
            
            income = float(df.iloc[0]['total_income'])
            expenses = float(df.iloc[0]['total_expenses'])
            net = float(df.iloc[0]['net_result'])
            count = int(df.iloc[0]['total_transactions'])
            stripe_count = int(df.iloc[0]['stripe_invoices'])
            invalid_count = int(df.iloc[0]['invalid_transactions'])
            
            profit_margin = (income / (income + expenses)) * 100 if (income + expenses) > 0 else 0
            
            return f"""
FINANCIAL SUMMARY

Revenue: ${income:,.2f}
Expenses: ${expenses:,.2f}
Net Profit: ${net:,.2f}
Profit Margin: {profit_margin:.1f}%

Transaction Details:
- Total Transactions: {count}
- STRIPE Invoices: {stripe_count}
- Invalid Transactions: {invalid_count}

{'Profitable!' if net > 0 else 'Operating at a loss'}
"""
        except Exception as e:
            return f"Analysis error: {str(e)}"

class TopCategoriesInput(BaseModel):
    transaction_type: str = Field(default="expense", description="'expense' or 'income' or 'both'")
    limit: int = Field(default=5, description="Number of top categories to show")

class TopCategoriesTools(BaseTool):
    name: str = "top_categories"
    description: str = "Get top expense or income categories with amounts and transaction counts"
    args_schema: Type[BaseModel] = TopCategoriesInput
    
    def _run(self, transaction_type: str = "expense", limit: int = 5) -> str:
        """Get top categories analysis"""
        try:
            engine = create_engine(DATABASE_URL)
            
            if transaction_type == "expense":
                where_clause = "WHERE amount < 0"
                amount_calc = "SUM(ABS(amount))"
                title = "TOP EXPENSE CATEGORIES"
            elif transaction_type == "income":
                where_clause = "WHERE amount > 0"
                amount_calc = "SUM(amount)"
                title = "TOP INCOME CATEGORIES"
            else:
                where_clause = ""
                amount_calc = "SUM(ABS(amount))"
                title = "TOP CATEGORIES (ALL)"
            
            query = f"""
            SELECT 
                category,
                {amount_calc} as total_amount,
                COUNT(*) as transaction_count,
                AVG(ABS(amount)) as avg_amount
            FROM ivy_data.transactions
            {where_clause}
            GROUP BY category
            ORDER BY {amount_calc} DESC
            LIMIT {limit}
            """
            
            df = pd.read_sql(query, engine)
            
            if df.empty:
                return f"No {transaction_type} transactions found."
            
            result = f"\n{title}\n\n"
            
            for i, row in df.iterrows():
                category = row['category']
                total = float(row['total_amount'])
                count = int(row['transaction_count'])
                avg = float(row['avg_amount'])
                
                result += f"{i+1}. {category}\n"
                result += f"   Total: ${total:,.2f}\n"
                result += f"   Transactions: {count}\n"
                result += f"   Average: ${avg:,.2f}\n\n"
            
            return result
        except Exception as e:
            return f"Categories analysis error: {str(e)}"

class StripeAnalysisInput(BaseModel):
    analysis_type: str = Field(default="summary", description="'summary', 'timeline', or 'types'")

class StripeAnalysisTool(BaseTool):
    name: str = "stripe_analysis"
    description: str = "Analyze STRIPE revenue: total revenue, invoice counts, timeline, revenue types"
    args_schema: Type[BaseModel] = StripeAnalysisInput
    
    def _run(self, analysis_type: str = "summary") -> str:
        """Get STRIPE revenue analysis"""
        try:
            engine = create_engine(DATABASE_URL)
            
            # Basic STRIPE summary
            summary_query = """
            SELECT 
                COUNT(*) as invoice_count,
                SUM(amount) as total_revenue,
                AVG(amount) as avg_invoice,
                MIN(date) as first_invoice,
                MAX(date) as latest_invoice
            FROM ivy_data.stripe_invoices
            """
            
            df = pd.read_sql(summary_query, engine)
            
            if df.empty or df.iloc[0]['invoice_count'] == 0:
                return "No STRIPE revenue transactions found."
            
            count = int(df.iloc[0]['invoice_count'])
            total = float(df.iloc[0]['total_revenue'])
            avg = float(df.iloc[0]['avg_invoice'])
            first = df.iloc[0]['first_invoice']
            latest = df.iloc[0]['latest_invoice']
            
            result = f"""
STRIPE REVENUE ANALYSIS

Summary:
- Total Invoices: {count}
- Total Revenue: ${total:,.2f}
- Average Invoice: ${avg:,.2f}
- First Invoice: {first}
- Latest Invoice: {latest}
"""
            
            if analysis_type == "timeline":
                # Monthly timeline
                timeline_query = """
                SELECT 
                    EXTRACT(YEAR FROM date) as year,
                    EXTRACT(MONTH FROM date) as month,
                    COUNT(*) as invoices,
                    SUM(amount) as monthly_revenue
                FROM ivy_data.stripe_invoices
                GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
                ORDER BY year, month
                """
                
                timeline_df = pd.read_sql(timeline_query, engine)
                result += "\nMonthly Timeline:\n"
                for _, row in timeline_df.iterrows():
                    year = int(row['year'])
                    month = int(row['month'])
                    invoices = int(row['invoices'])
                    revenue = float(row['monthly_revenue'])
                    result += f"- {month:02d}/{year}: {invoices} invoices, ${revenue:,.2f}\n"
            
            return result
        except Exception as e:
            return f"STRIPE analysis error: {str(e)}"

def create_financial_agent():
    """Create LangChain agent with financial tools and SQL capabilities"""
    
    # Check for OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        raise ValueError("Please set your OPENAI_API_KEY in the .env file")
    
    # Initialize OpenAI
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",  # Using 3.5-turbo for cost efficiency
        temperature=0.1,
        openai_api_key=openai_key
    )
    
    # Create SQL database connection for LangChain
    try:
        db = SQLDatabase.from_uri(DATABASE_URL)
        
        # Create SQL toolkit
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        # Custom financial tools
        custom_tools = [
            TransactionQueryTool(),
            FinancialSummaryTool(),
            TopCategoriesTools(),
            StripeAnalysisTool()
        ]
        
        # Create agent with both SQL tools and custom tools
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            extra_tools=custom_tools,
            verbose=False,
            agent_type="openai-tools",
            max_iterations=3,
            max_execution_time=30
        )
        
        return agent
        
    except Exception as e:
        raise Exception(f"Failed to create agent: {str(e)}")

def chat_with_financial_data(question: str) -> str:
    """Main function to chat with financial data"""
    try:
        # Convert question to lowercase for keyword matching
        q_lower = question.lower()
        
        # Route to appropriate tool based on question keywords
        if any(word in q_lower for word in ['summary', 'total', 'revenue', 'expenses', 'profit', 'overview']):
            tool = FinancialSummaryTool()
            return tool._run("all")
            
        elif any(word in q_lower for word in ['categories', 'category', 'expense', 'top', 'biggest', 'largest']):
            tool = TopCategoriesTools()
            if 'income' in q_lower:
                return tool._run("income", 5)
            else:
                return tool._run("expense", 5)
                
        elif any(word in q_lower for word in ['stripe', 'payment', 'invoice', 'revenue']):
            tool = StripeAnalysisTool()
            return tool._run("summary")
            
        elif any(word in q_lower for word in ['transactions', 'count', 'how many', 'number']):
            tool = TransactionQueryTool()
            return tool._run("SELECT COUNT(*) as total_transactions, SUM(amount) as net_amount FROM ivy_data.transactions;")
            
        elif any(word in q_lower for word in ['invalid', 'problems', 'issues', 'quality']):
            tool = TransactionQueryTool()
            return tool._run("SELECT COUNT(*) as invalid_count FROM ivy_data.transactions WHERE is_invalid = true;")
            
        elif any(word in q_lower for word in ['month', 'monthly', 'trend']):
            tool = TransactionQueryTool()
            return tool._run("""
                SELECT 
                    EXTRACT(YEAR FROM date) as year,
                    EXTRACT(MONTH FROM date) as month,
                    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
                    SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as expenses,
                    SUM(amount) as net
                FROM ivy_data.transactions 
                GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
                ORDER BY year DESC, month DESC
                LIMIT 6;
            """)
            
        else:
            # For other questions, use OpenAI with our data summary
            from langchain_openai import ChatOpenAI
            
            # Get data summary first
            summary_tool = FinancialSummaryTool()
            financial_summary = summary_tool._run("all")
            
            categories_tool = TopCategoriesTools()
            top_expenses = categories_tool._run("expense", 3)
            
            # Use OpenAI for natural language response
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.1,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            prompt = f"""
You are a financial analyst. Based on this company's financial data, answer the user's question:

FINANCIAL DATA:
{financial_summary}

TOP EXPENSES:
{top_expenses}

USER QUESTION: {question}

Provide a helpful, concise answer based on this data. If you need specific data not provided, say so.
"""
            
            response = llm.invoke(prompt)
            return response.content
            
    except Exception as e:
        return f"I encountered an error while analyzing your financial data: {str(e)}"