import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="sabrina"
)

cursor = conn.cursor()
cursor.execute("DROP SCHEMA IF EXISTS ivy_data CASCADE;")
conn.commit()
cursor.close()
conn.close()
print("✅ Schema ivy_data removed")