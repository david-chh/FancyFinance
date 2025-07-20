"""
Setup script for the AI Financial Chatbot
Helps you configure OpenAI API key and test the integration
"""

import os

from dotenv import load_dotenv, set_key


def setup_openai_key():
    """Setup OpenAI API key"""
    print("OpenAI API Key Setup")
    print("=" * 40)

    # Check if .env exists
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"Creating {env_file} file...")
        with open(env_file, "w") as f:
            f.write("# OpenAI API Configuration\n")
            f.write(
                "OPENAI_API_KEY=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\n\n"
            )
            f.write("# Database Configuration\n")
            f.write(
                "DATABASE_URL=postgresql://postgres.njyncmeeqjrtultxcpgb:xtz1KQD-btj8nzf5gtz@aws-0-eu-central-1.pooler.supabase.com:5432/postgres\n"
            )

    # Load current values
    load_dotenv()
    current_key = os.getenv("OPENAI_API_KEY", "")

    if current_key and current_key != "your_openai_api_key_here":
        print(f"OpenAI API key already configured: {current_key[:10]}...")
        update = input("Do you want to update it? (y/n): ").lower().strip()
        if update != "y":
            return current_key

    print("\nTo get your OpenAI API key:")
    print("1. Go to https://platform.openai.com/api-keys")
    print("2. Create a new API key")
    print("3. Copy the key (starts with 'sk-')")
    print()

    while True:
        api_key = input("Enter your OpenAI API key: ").strip()

        if not api_key:
            print("ERROR: Please enter a valid API key")
            continue

        if not api_key.startswith("sk-"):
            print("ERROR: OpenAI API keys should start with 'sk-'")
            continue

        if len(api_key) < 20:
            print("ERROR: API key seems too short")
            continue

        # Save to .env file
        set_key(env_file, "OPENAI_API_KEY", api_key)
        print(f"API key saved to {env_file}")
        return api_key


def test_dependencies():
    """Test if all required packages are installed"""
    print("Checking Dependencies")
    print("=" * 40)

    required_packages = [
        ("langchain", "langchain"),
        ("langchain_openai", "langchain-openai"),
        ("openai", "openai"),
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("sqlalchemy", "sqlalchemy"),
        ("psycopg2", "psycopg2-binary"),
        ("plotly", "plotly"),
        # ("python-dotenv", "python-dotenv"),
    ]

    missing_packages = []

    for package_name, install_name in required_packages:
        try:
            __import__(package_name)
            print(f"OK: {package_name}")
        except ImportError:
            print(f"MISSING: {package_name}")
            missing_packages.append(install_name)

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run this command to install them:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    else:
        print("\nAll dependencies are installed!")
        return True


# def test_database_connection():
#     """Test database connection"""
#     print("Testing Database Connection")
#     print("=" * 40)

#     try:
#         import psycopg2
#         from dotenv import load_dotenv

#         load_dotenv()

#         db_url = os.getenv("DATABASE_URL")
#         if not db_url:
#             print("ERROR: DATABASE_URL not found in .env file")
#             return False

#         # Test connection
#         conn = psycopg2.connect(db_url)
#         cursor = conn.cursor()

#         # Test if our tables exist
#         cursor.execute("""
#             SELECT table_name
#             FROM information_schema.tables
#             WHERE table_schema = 'ivy_data'
#         """)

#         tables = [row[0] for row in cursor.fetchall()]

#         if "transactions" in tables:
#             print("Database connection successful")
#             print(f"Found tables: {', '.join(tables)}")

#             # Get transaction count
#             cursor.execute("SELECT COUNT(*) FROM ivy_data.transactions")
#             count = cursor.fetchone()[0]
#             print(f"Transaction records: {count}")

#         else:
#             print("ERROR: Transaction tables not found")
#             print("Run 'python dlt_pipeline.py' first to load data")
#             return False

#         cursor.close()
#         conn.close()
#         return True

#     except Exception as e:
#         print(f"ERROR: Database connection failed: {e}")
#         return False


def test_openai_connection():
    """Test OpenAI connection"""
    print("Testing OpenAI Connection")
    print("=" * 40)

    try:
        from dotenv import load_dotenv

        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            print("ERROR: OpenAI API key not configured")
            return False

        # Test API call
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello! Just testing the connection."}
            ],
            max_tokens=50,
        )

        print("OpenAI API connection successful")
        print(f"Test response: {response.choices[0].message.content[:50]}...")
        return True

    except Exception as e:
        print(f"ERROR: OpenAI connection failed: {e}")
        print("Check your API key and account balance")
        return False


def test_full_integration():
    """Test the full chatbot integration"""
    print("Testing Full Integration")
    print("=" * 40)

    try:
        from src.langchain_tools import chat_with_financial_data

        test_question = "How many transactions do I have?"
        print(f"Testing question: '{test_question}'")

        response = chat_with_financial_data(test_question)
        print(f"AI Response: {response[:100]}...")

        return True

    except Exception as e:
        print(f"ERROR: Integration test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("IVY Financial AI Chatbot Setup")
    print("=" * 50)

    # Step 1: Check dependencies
    if not test_dependencies():
        print("\nPlease install missing dependencies first")
        return

    # Step 2: Setup OpenAI API key
    api_key = setup_openai_key()
    if not api_key:
        print("\nOpenAI API key setup failed")
        return

    print()

    # # Step 3: Test database
    # if not test_database_connection():
    #     print("\nDatabase setup incomplete")
    #     return

    # print()

    # Step 4: Test OpenAI
    if not test_openai_connection():
        print("\nOpenAI setup failed")
        return

    print()

    # Step 5: Test full integration
    if not test_full_integration():
        print("\nIntegration test failed")
        return

    print("\nSETUP COMPLETE!")
    print("=" * 50)
    print("All systems ready!")
    print()
    print("Next steps:")
    print("1. Run 'streamlit run dashboard.py' to start the dashboard")
    print("2. Navigate to the AI Assistant section")
    print("3. Start asking questions about your financial data!")
    print()
    print("Example questions to try:")
    print("- 'What's my total profit?'")
    print("- 'Show me my top expense categories'")
    print("- 'How much STRIPE revenue do I have?'")


if __name__ == "__main__":
    main()
