#!/usr/bin/env python3
"""
FancyFinance Dashboard Entry Point
Run this script to start the Streamlit dashboard from the root directory
"""

import os
import sys
import subprocess

def main():
    """Start the Streamlit dashboard"""
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the dashboard
    dashboard_path = os.path.join(script_dir, "src", "dashboard.py")
    
    # Check if dashboard exists
    if not os.path.exists(dashboard_path):
        print("❌ Error: Dashboard not found at", dashboard_path)
        return 1
    
    # Run streamlit
    print("🚀 Starting FancyFinance Dashboard...")
    print("📊 Dashboard will open at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", dashboard_path
        ], cwd=script_dir)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped!")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())