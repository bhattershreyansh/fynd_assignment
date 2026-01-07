import sys
import os

# Add the current directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ai_service import ai_service
    print("✅ AI Service imported successfully!")
    
    # Test initialization
    print(f"Model configured: {ai_service.model}")
    
    # Simulate a call (this will likely fail if no real API key is present in this env, but we can check the error handling)
    print("\nAttempting a test generation (might fail if API key is invalid)...")
    try:
        response = ai_service.generate_user_response("Test User", 5, "Great service!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Expected failure or error: {str(e)}")

except ImportError as e:
    print(f"❌ Import error: {str(e)}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
