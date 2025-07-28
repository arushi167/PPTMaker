#!/usr/bin/env python3
"""
Test script for Gemini API integration
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the Gemini API integration"""
    
    # Get API key from environment
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please set GEMINI_API_KEY in your .env file")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Test prompt
        test_prompt = "Write a brief introduction for a presentation about artificial intelligence (2-3 sentences only)"
        
        print("🤖 Testing Gemini API...")
        print(f"Prompt: {test_prompt}")
        print("-" * 50)
        
        # Generate response
        response = model.generate_content(test_prompt)
        
        print("✅ Gemini API Test Successful!")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API Test Failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api() 