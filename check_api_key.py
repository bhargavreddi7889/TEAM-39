"""
Check OpenAI API Key Status and Quota
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

def check_openai_key():
    """Check if OpenAI API key is valid and has quota."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("=" * 60)
    print("CHECKING OPENAI API KEY STATUS")
    print("=" * 60)
    print()
    
    if not api_key:
        print("[ERROR] No OPENAI_API_KEY found in .env file")
        print("        Please add your API key to the .env file")
        return False
    
    # Mask the key for display
    masked_key = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
    print(f"API Key: {masked_key}")
    print()
    
    try:
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        # Test 1: Simple completion test
        print("Test 1: Testing Chat Completion...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API key is working!'"}],
            max_tokens=20
        )
        print(f"[SUCCESS] Chat Completion works!")
        print(f"          Response: {response.choices[0].message.content}")
        print()
        
        # Test 2: Embeddings test
        print("Test 2: Testing Embeddings...")
        embedding_response = client.embeddings.create(
            model="text-embedding-3-small",
            input="Test embedding"
        )
        embedding_dim = len(embedding_response.data[0].embedding)
        print(f"[SUCCESS] Embeddings work!")
        print(f"          Embedding dimension: {embedding_dim}")
        print()
        
        # Success
        print("=" * 60)
        print("[SUCCESS] ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("Your OpenAI API key is VALID and has QUOTA available!")
        print("You can now run the application: python run.py")
        print()
        return True
        
    except Exception as e:
        error_str = str(e)
        print("=" * 60)
        print("❌ API KEY CHECK FAILED")
        print("=" * 60)
        print()
        print(f"Error: {error_str}")
        print()
        
        # Check for specific errors
        if "429" in error_str or "insufficient_quota" in error_str:
            print("[QUOTA ISSUE] Your API key has NO remaining quota/credits")
            print()
            print("How to fix:")
            print("  1. Go to: https://platform.openai.com/account/billing")
            print("  2. Add payment method and credits")
            print("  3. Wait a few minutes for credits to activate")
            print("  4. Run this script again to verify")
            print()
        elif "401" in error_str or "Incorrect API key" in error_str:
            print("[INVALID KEY] Your API key is not valid or revoked")
            print()
            print("How to fix:")
            print("  1. Go to: https://platform.openai.com/api-keys")
            print("  2. Create a new API key")
            print("  3. Update your .env file with the new key")
            print("  4. Run this script again to verify")
            print()
        elif "403" in error_str:
            print("[PERMISSION DENIED] API key lacks required permissions")
            print()
        else:
            print("[UNKNOWN ERROR] Check your internet and API key")
            print()
        
        return False

if __name__ == "__main__":
    print()
    openai_ok = check_openai_key()
    print()
    
    if openai_ok:
        print("=" * 60)
        print("[SUCCESS] YOUR SETUP IS READY!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Make sure you have documents in the 'data/' folder")
        print("  2. Run: python run.py")
        print("  3. Access the UI at: http://localhost:8501")
        print()
        sys.exit(0)
    else:
        print("=" * 60)
        print("[FAILED] SETUP INCOMPLETE - Fix the issues above")
        print("=" * 60)
        sys.exit(1)

