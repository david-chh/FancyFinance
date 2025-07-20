"""
CSV file debug to understand format
"""

import pandas as pd
import csv

def debug_csv():
    """CSV Debug"""
    
    print("=== CSV DEBUG ===")
    
    # Method 1: Read first lines as text
    with open("IVY Transaction Data - Sheet1.csv", 'r', encoding='utf-8') as file:
        print("📄 First 3 lines of file:")
        for i, line in enumerate(file):
            if i < 3:
                print(f"Line {i+1}: {repr(line)}")
    
    print("\n" + "="*50)
    
    # Method 2: Use csv.reader
    print("📊 Using csv.reader:")
    with open("IVY Transaction Data - Sheet1.csv", 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i < 3:
                print(f"Line {i+1}: {len(row)} columns -> {row}")
    
    print("\n" + "="*50)
    
    # Method 3: Try different delimiters
    delimiters = [',', ';', '\t', '|']
    for delim in delimiters:
        try:
            print(f"🔧 Testing delimiter '{delim}':")
            df = pd.read_csv("IVY Transaction Data - Sheet1.csv", sep=delim, nrows=2)
            print(f"   Columns: {len(df.columns)} -> {list(df.columns)}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n" + "="*50)
    
    # Method 4: Force manual split
    print("✂️ Manual split on first line:")
    with open("IVY Transaction Data - Sheet1.csv", 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
        print(f"Original line: {repr(first_line)}")
        
        # Remove outer quotes if they exist
        if first_line.startswith('"') and first_line.endswith('"'):
            first_line = first_line[1:-1]
            print(f"Without quotes: {repr(first_line)}")
        
        # Split by comma
        parts = first_line.split(',')
        print(f"Split by comma: {len(parts)} parts -> {parts}")

if __name__ == "__main__":
    debug_csv()