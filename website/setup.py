#!/usr/bin/env python3
"""
FancyFinance Setup Script
Quick setup wizard for first-time users
"""

import os
import sys
import shutil

def create_env_file():
    """Create .env file from template"""
    env_example = "config/.env.example"
    env_file = ".env"
    
    if os.path.exists(env_file):
        response = input(f"⚠️  {env_file} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env creation")
            return
    
    if os.path.exists(env_example):
        shutil.copy2(env_example, env_file)
        print(f"✅ Created {env_file} from template")
        print("📝 Please edit .env with your actual API keys and database URL")
    else:
        print(f"❌ Template {env_example} not found")

def create_dlt_secrets():
    """Create DLT secrets file from template"""
    secrets_example = "config/secrets.toml.example"
    secrets_dir = ".dlt"
    secrets_file = ".dlt/secrets.toml"
    
    # Create .dlt directory if it doesn't exist
    if not os.path.exists(secrets_dir):
        os.makedirs(secrets_dir)
        print(f"✅ Created {secrets_dir} directory")
    
    if os.path.exists(secrets_file):
        response = input(f"⚠️  {secrets_file} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping secrets.toml creation")
            return
    
    if os.path.exists(secrets_example):
        shutil.copy2(secrets_example, secrets_file)
        print(f"✅ Created {secrets_file} from template")
        print("📝 Please edit .dlt/secrets.toml with your database credentials")
    else:
        print(f"❌ Template {secrets_example} not found")

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ Core dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 FancyFinance Setup Wizard")
    print("=" * 50)
    
    # Check current directory
    if not os.path.exists("src/dashboard.py"):
        print("❌ Error: Please run this script from the FancyFinance root directory")
        return 1
    
    print("📂 Found FancyFinance project structure")
    
    # Create configuration files
    print("\n📝 Setting up configuration files...")
    create_env_file()
    create_dlt_secrets()
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        return 1
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env with your OpenAI API key and database URL")
    print("2. Edit .dlt/secrets.toml with your database credentials")
    print("3. Run: python src/dlt_pipeline.py (to load data)")
    print("4. Run: python run_dashboard.py (to start dashboard)")
    print("\n📖 See README.md for detailed instructions")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())