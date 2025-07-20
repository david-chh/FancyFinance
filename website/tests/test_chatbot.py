"""
Test the LangChain chatbot integration
Run this to verify OpenAI + database integration works
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.langchain_tools import chat_with_financial_data

load_dotenv()

def test_questions():
    """Test various financial questions"""
    
    print("Testing Financial AI Assistant")
    print("=" * 50)
    
    # Check API key first
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("ERROR: Please set your OPENAI_API_KEY in the .env file")
        print("Get your API key from: https://platform.openai.com/api-keys")
        return
    
    print(f"OpenAI API Key found: {api_key[:10]}...")
    print()
    
    # Test questions from simple to complex
    questions = [
        "What's my total revenue and expenses?",
        "What are my top 3 expense categories?", 
        "How much STRIPE revenue did I receive?",
        "Show me transactions over $1000",
        "Are there any invalid transactions I should review?",
        "What's my profit margin?",
        "Which month had the highest revenue?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"Q{i}: {question}")
        print("-" * 40)
        
        try:
            response = chat_with_financial_data(question)
            print(f"A{i}: {response}")
            print()
            
        except Exception as e:
            print(f"ERROR: {e}")
            print()
        
        # Add a small delay between questions
        import time
        time.sleep(1)

def test_simple_connection():
    """Test basic database connection"""
    print("Testing database connection...")
    
    try:
        from src.langchain_tools import create_financial_agent
        agent = create_financial_agent()
        print("Agent created successfully!")
        
        # Simple test question
        response = chat_with_financial_data("How many transactions do I have?")
        print(f"Test response: {response[:100]}...")
        
    except Exception as e:
        print(f"Connection test failed: {e}")

if __name__ == "__main__":
    print("CHATBOT INTEGRATION TEST")
    print("=" * 50)
    
    # Quick connection test first
    test_simple_connection()
    print()
    
    # Full question test
    test_questions()
    
    print("Testing completed!")
    print("\nIf tests passed, your chatbot is ready!")
    print("Next step: Run 'streamlit run dashboard.py' to see it in action.")