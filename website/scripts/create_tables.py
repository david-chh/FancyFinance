"""
Script to create necessary tables in Supabase
"""

import psycopg2
from psycopg2 import sql

def create_tables():
    """Creates necessary tables for the pipeline"""
    
    connection_string = "postgresql://postgres.njyncmeeqjrtultxcpgb:xtz1KQD-btj8nzf5gtz@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"
    
    # SQLs to create tables
    create_tables_sql = [
        """
        CREATE SCHEMA IF NOT EXISTS ivy_data;
        """,
        """
        CREATE TABLE IF NOT EXISTS ivy_data.transactions (
            transaction_id VARCHAR(50) PRIMARY KEY,
            date DATE NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            reference VARCHAR(100),
            category VARCHAR(100),
            currency VARCHAR(3),
            counterparty VARCHAR(200),
            provider VARCHAR(100),
            transaction_type VARCHAR(10),
            month_year VARCHAR(7),
            is_stripe_invoice BOOLEAN DEFAULT FALSE,
            is_invalid BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ivy_data.stripe_invoices (
            transaction_id VARCHAR(50) PRIMARY KEY,
            date DATE NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            reference VARCHAR(100),
            category VARCHAR(100),
            currency VARCHAR(3),
            counterparty VARCHAR(200),
            provider VARCHAR(100),
            invoice_number VARCHAR(50),
            invoice_type VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ivy_data.category_summary (
            category VARCHAR(100) PRIMARY KEY,
            total_amount DECIMAL(12,2),
            transaction_count INTEGER,
            avg_amount DECIMAL(10,2),
            total_transactions INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_transactions_date ON ivy_data.transactions(date);
        CREATE INDEX IF NOT EXISTS idx_transactions_category ON ivy_data.transactions(category);
        CREATE INDEX IF NOT EXISTS idx_transactions_amount ON ivy_data.transactions(amount);
        CREATE INDEX IF NOT EXISTS idx_transactions_type ON ivy_data.transactions(transaction_type);
        CREATE INDEX IF NOT EXISTS idx_stripe_date ON ivy_data.stripe_invoices(date);
        """
    ]
    
    try:
        print("🔄 Connecting to Supabase...")
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        print("✅ Connection established!")
        
        for i, sql_statement in enumerate(create_tables_sql, 1):
            print(f"📊 Executing SQL {i}/{len(create_tables_sql)}...")
            cursor.execute(sql_statement)
            conn.commit()
        
        print("✅ All tables created successfully!")
        
        # Check created tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'ivy_data'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"📋 Tables created in ivy_data schema: {[t[0] for t in tables]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    create_tables()