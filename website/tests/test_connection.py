"""
Script para testar conexão com Supabase PostgreSQL
"""

import psycopg2
from psycopg2 import sql
import sys

def test_supabase_connection():
    """Testa conexão com Supabase"""
    
    # Configurações Supabase
    config = {
        "host": "db.njyncmeeqjrtultxcpgb.supabase.co",
        "port": 5432,
        "database": "postgres",
        "user": "postgres",
        "password": "xtz1KQD-btj8nzf5gtz"
    }
    
    try:
        print("🔄 Tentando conectar no Supabase...")
        
        # Tenta conexão
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        print("✅ Conexão estabelecida com sucesso!")
        
        # Testa uma query simples
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 Versão PostgreSQL: {version[0]}")
        
        # Lista schemas disponíveis
        cursor.execute("SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;")
        schemas = cursor.fetchall()
        print(f"📁 Schemas disponíveis: {[s[0] for s in schemas]}")
        
        # Lista tabelas no schema public
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"📋 Tabelas existentes: {[t[0] for t in tables] if tables else 'Nenhuma'}")
        
        cursor.close()
        conn.close()
        
        print("✅ Teste de conexão concluído com sucesso!")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erro de conexão PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    test_supabase_connection()