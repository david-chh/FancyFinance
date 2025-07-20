"""
Simple pipeline to test data loading
"""

import pandas as pd
import psycopg2
from datetime import datetime

def simple_load():
    """Loads data directly to PostgreSQL without DLT"""
    
    # Load CSV removing extra quotes
    print("📊 Loading CSV...")
    
    # Read file and remove extra quotes from each line
    processed_data = []
    with open("IVY Transaction Data - Sheet1.csv", 'r', encoding='utf-8') as file:
        for line in file:
            # Remove line break and outer quotes
            clean_line = line.strip()
            if clean_line.startswith('"') and clean_line.endswith('"'):
                clean_line = clean_line[1:-1]
            # Split by comma
            row = clean_line.split(',')
            processed_data.append(row)
    
    # Create DataFrame
    headers = processed_data[0]
    rows = processed_data[1:]
    df = pd.DataFrame(rows, columns=headers)
    
    # Show basic info
    print(f"✅ Data loaded: {len(df)} rows")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Normalize columns
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    print(f"📋 Normalized columns: {list(df.columns)}")
    
    # Process data (now the column is 'date' after normalization)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['transaction_type'] = df['amount'].apply(lambda x: 'income' if x > 0 else 'expense')
    df['is_stripe_invoice'] = df['reference'].str.contains('STRIPE-', na=False)
    
    # Connect PostgreSQL
    print("🔄 Connecting PostgreSQL...")
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="sabrina"
    )
    
    # Create schema
    cursor = conn.cursor()
    cursor.execute("CREATE SCHEMA IF NOT EXISTS ivy_data;")
    conn.commit()
    
    # Load data using pandas to_sql
    print("📤 Loading data...")
    from sqlalchemy import create_engine
    
    engine = create_engine("postgresql://postgres:sabrina@localhost:5432/postgres")
    
    # Load main table
    df.to_sql('transactions', engine, schema='ivy_data', if_exists='replace', index=False)
    
    # Create STRIPE invoices table
    stripe_df = df[df['is_stripe_invoice'] == True].copy()
    stripe_df['invoice_number'] = stripe_df['reference'].str.extract(r'STRIPE-(\d+)')
    stripe_df.to_sql('stripe_invoices', engine, schema='ivy_data', if_exists='replace', index=False)
    
    # Summary by category
    category_summary = df.groupby('category').agg({
        'amount': ['sum', 'count', 'mean']
    }).round(2)
    category_summary.columns = ['total_amount', 'transaction_count', 'avg_amount']
    category_summary = category_summary.reset_index()
    category_summary.to_sql('category_summary', engine, schema='ivy_data', if_exists='replace', index=False)
    
    print("✅ Data loaded successfully!")
    
    # Basic analytics
    print("\\n=== BASIC ANALYTICS ===")
    
    # Total income vs expenses
    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expenses = df[df['amount'] < 0]['amount'].abs().sum()
    print(f"💰 Total Income: ${total_income:,.2f}")
    print(f"💸 Total Expenses: ${total_expenses:,.2f}")
    print(f"📊 Net: ${total_income - total_expenses:,.2f}")
    
    # Top categories
    print("\\n📋 Top 5 Categories (Expenses):")
    top_expenses = df[df['amount'] < 0].groupby('category')['amount'].sum().abs().sort_values(ascending=False).head(5)
    for cat, amount in top_expenses.items():
        print(f"  {cat}: ${amount:,.2f}")
    
    # STRIPE Invoices
    stripe_total = df[df['is_stripe_invoice'] == True]['amount'].sum()
    stripe_count = df[df['is_stripe_invoice'] == True].shape[0]
    print(f"\\n💳 STRIPE Invoices: {stripe_count} transactions, Total: ${stripe_total:,.2f}")
    
    # Invalid transactions
    invalid_count = df[df['amount'].isna() | df['description'].isna()].shape[0]
    print(f"⚠️ Invalid transactions: {invalid_count}")
    
    cursor.close()
    conn.close()
    
    print("\\n🎉 Pipeline completed!")

if __name__ == "__main__":
    simple_load()