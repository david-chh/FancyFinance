"""
Simple test of our financial AI tools without the complex SQL agent
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.langchain_tools import (
    FinancialSummaryTool, 
    TopCategoriesTools, 
    StripeAnalysisTool,
    TransactionQueryTool
)

load_dotenv()

def test_tools():
    """Test each tool individually"""
    
    print("FINANCIAL AI TOOLS TEST")
    print("=" * 50)
    
    # Test Financial Summary
    print("\n1. FINANCIAL SUMMARY")
    print("-" * 30)
    summary_tool = FinancialSummaryTool()
    result = summary_tool._run("all")
    print(result)
    
    # Test Top Categories
    print("\n2. TOP EXPENSE CATEGORIES")
    print("-" * 30)
    categories_tool = TopCategoriesTools()
    result = categories_tool._run("expense", 5)
    print(result)
    
    # Test STRIPE Analysis
    print("\n3. STRIPE ANALYSIS")
    print("-" * 30)
    stripe_tool = StripeAnalysisTool()
    result = stripe_tool._run("summary")
    print(result)
    
    # Test Direct Query
    print("\n4. DIRECT QUERY TEST")
    print("-" * 30)
    query_tool = TransactionQueryTool()
    result = query_tool._run("SELECT COUNT(*) as total_transactions, SUM(amount) as total_amount FROM ivy_data.transactions;")
    print(result)

if __name__ == "__main__":
    test_tools()