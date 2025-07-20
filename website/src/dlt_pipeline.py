"""
DLT Pipeline to load transaction data from Excel to PostgreSQL
with normalization and invalid transaction analysis
"""

import dlt
import pandas as pd
from typing import Iterator, Dict, Any
import os
from datetime import datetime
import re

# Pipeline configuration
@dlt.source
def ivy_transactions_source():
    """Source to load IVY transaction data"""
    
    def load_transactions() -> Iterator[Dict[str, Any]]:
        """Loads and normalizes transaction data"""
        # Load CSV with custom parser (removes extra quotes)
        processed_data = []
        with open("IVY Transaction Data - Sheet1.csv", 'r', encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                if clean_line.startswith('"') and clean_line.endswith('"'):
                    clean_line = clean_line[1:-1]
                row = clean_line.split(',')
                processed_data.append(row)
        
        # Create DataFrame
        headers = processed_data[0]
        rows = processed_data[1:]
        df = pd.DataFrame(rows, columns=headers)
        
        # Basic normalization
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Convert amount to float
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Add calculated columns
        df['transaction_type'] = df['amount'].apply(lambda x: 'income' if x > 0 else 'expense')
        df['month_year'] = df['date'].dt.to_period('M').astype(str)
        df['is_stripe_invoice'] = df['reference'].str.contains('STRIPE-', na=False)
        
        # Invalid transaction detection
        df['is_invalid'] = (
            df['amount'].isna() | 
            df['description'].isna() | 
            df['category'].isna() |
            (df['amount'] == 0)
        )
        
        # Convert to dictionaries
        for _, row in df.iterrows():
            yield row.to_dict()
    
    def load_stripe_invoices() -> Iterator[Dict[str, Any]]:
        """Extracts and processes STRIPE invoices separately"""
        # Use same parser
        processed_data = []
        with open("IVY Transaction Data - Sheet1.csv", 'r', encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                if clean_line.startswith('"') and clean_line.endswith('"'):
                    clean_line = clean_line[1:-1]
                row = clean_line.split(',')
                processed_data.append(row)
        
        headers = processed_data[0]
        rows = processed_data[1:]
        df = pd.DataFrame(rows, columns=headers)
        
        # Filter only STRIPE transactions (invoices)
        stripe_df = df[df['Reference'].str.contains('STRIPE-', na=False)].copy()
        
        # Normalization
        stripe_df.columns = stripe_df.columns.str.lower().str.replace(' ', '_')
        stripe_df['date'] = pd.to_datetime(stripe_df['date'])
        stripe_df['amount'] = pd.to_numeric(stripe_df['amount'], errors='coerce')
        
        # Extract invoice number
        stripe_df['invoice_number'] = stripe_df['reference'].str.extract(r'STRIPE-(\d+)')
        stripe_df['invoice_type'] = stripe_df['description'].str.extract(r'(.*?)\s+(payment|revenue)', expand=False)[0]
        
        for _, row in stripe_df.iterrows():
            yield row.to_dict()
    
    def load_category_summary() -> Iterator[Dict[str, Any]]:
        """Cria resumo por categoria"""
        # Usa mesmo parser
        processed_data = []
        with open("IVY Transaction Data - Sheet1.csv", 'r', encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                if clean_line.startswith('"') and clean_line.endswith('"'):
                    clean_line = clean_line[1:-1]
                row = clean_line.split(',')
                processed_data.append(row)
        
        headers = processed_data[0]
        rows = processed_data[1:]
        df = pd.DataFrame(rows, columns=headers)
        
        # Converte Amount para numérico antes da agregação
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        
        # Agrupa por categoria
        summary = df.groupby('Category').agg({
            'Amount': ['sum', 'count', 'mean'],
            'Transaction ID': 'count'
        }).round(2)
        
        summary.columns = ['total_amount', 'transaction_count', 'avg_amount', 'total_transactions']
        summary = summary.reset_index()
        summary.columns = summary.columns.str.lower().str.replace(' ', '_')
        
        for _, row in summary.iterrows():
            yield row.to_dict()
    
    return (
        dlt.resource(load_transactions, name="transactions", write_disposition="replace"),
        dlt.resource(load_stripe_invoices, name="stripe_invoices", write_disposition="replace")
    )

def run_pipeline():
    """Executes the DLT pipeline"""
    
    # Create pipeline (credentials in .dlt/secrets.toml)
    pipeline = dlt.pipeline(
        pipeline_name="ivy_transactions",
        destination="postgres",
        dataset_name="ivy_data"
    )
    
    # Execute the load
    load_info = pipeline.run(ivy_transactions_source())
    
    print(f"Pipeline executed successfully!")
    print(f"Loads: {load_info}")
    
    return pipeline

def run_analytics_queries(pipeline):
    """Runs analytical queries for dashboard insights"""
    
    with pipeline.sql_client() as client:
        
        # 1. Monthly financial summary
        monthly_summary = client.execute_sql("""
            SELECT 
                EXTRACT(YEAR FROM date) as year,
                EXTRACT(MONTH FROM date) as month,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as total_expenses,
                SUM(amount) as net_amount,
                COUNT(*) as transaction_count
            FROM ivy_data.transactions
            GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
            ORDER BY year DESC, month DESC
        """)
        
        print("\\n=== MONTHLY FINANCIAL SUMMARY ===")
        for row in monthly_summary:
            print(f"{int(row[1]):02d}/{int(row[0])}: Income=${row[2]:,.2f}, Expenses=${row[3]:,.2f}, Net=${row[4]:,.2f}, Transactions={row[5]}")
        
        # 2. Top expense categories
        category_expenses = client.execute_sql("""
            SELECT 
                category,
                SUM(ABS(amount)) as total_spent,
                COUNT(*) as transaction_count,
                AVG(ABS(amount)) as avg_transaction
            FROM ivy_data.transactions
            WHERE amount < 0
            GROUP BY category
            ORDER BY total_spent DESC
            LIMIT 10
        """)
        
        print("\\n=== TOP 10 EXPENSE CATEGORIES ===")
        for row in category_expenses:
            print(f"{row[0]}: ${row[1]:,.2f} ({row[2]} transactions, avg=${row[3]:,.2f})")
        
        # 3. STRIPE revenue analysis
        stripe_analysis = client.execute_sql("""
            SELECT 
                invoice_type,
                COUNT(*) as invoice_count,
                SUM(amount) as total_revenue,
                AVG(amount) as avg_revenue,
                MIN(date) as first_invoice,
                MAX(date) as last_invoice
            FROM ivy_data.stripe_invoices
            GROUP BY invoice_type
            ORDER BY total_revenue DESC
        """)
        
        print("\\n=== STRIPE REVENUE ANALYSIS ===")
        for row in stripe_analysis:
            print(f"{row[0]}: ${row[2]:,.2f} ({row[1]} invoices, avg=${row[3]:,.2f})")
        
        # 4. Invalid transactions
        invalid_transactions = client.execute_sql("""
            SELECT 
                COUNT(*) as total_invalid,
                COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ivy_data.transactions) as invalid_percentage
            FROM ivy_data.transactions
            WHERE is_invalid = true
        """)
        
        print("\\n=== INVALID TRANSACTIONS ===")
        for row in invalid_transactions:
            print(f"Total invalid: {row[0]} ({row[1]:.2f}%)")
        
        # 5. Monthly trends
        trends = client.execute_sql("""
            SELECT 
                month_year,
                COUNT(*) as transactions,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as expenses
            FROM ivy_data.transactions
            GROUP BY month_year
            ORDER BY month_year DESC
            LIMIT 6
        """)
        
        print("\\n=== LAST 6 MONTHS TRENDS ===")
        for row in trends:
            print(f"{row[0]}: {row[1]} transactions, Income=${row[2]:,.2f}, Expenses=${row[3]:,.2f}")

if __name__ == "__main__":
    # Execute pipeline
    pipeline = run_pipeline()
    
    # Execute analytics
    run_analytics_queries(pipeline)
    
    print("\\nPipeline and analytics completed!")
    print("\\nNext steps for dashboard:")
    print("1. Connect BI tool (Grafana, PowerBI, etc.) to PostgreSQL")
    print("2. Use tables: transactions, stripe_invoices, category_summary")
    print("3. Implement alerts for invalid transactions")
    print("4. Create KPI metrics based on analytical queries")