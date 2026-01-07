"""
Test script using Groq API for rating prediction
Tests with 5 reviews to validate the setup
"""

import os
from groq import Groq
import pandas as pd
import json
import time
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
print("✓ Groq client initialized")

# Load sample data
df = pd.read_csv('yelp.csv')
df_test = df.sample(n=5, random_state=42).reset_index(drop=True)
print(f"✓ Loaded {len(df_test)} test reviews")

# Define test prompt
PROMPT_TEMPLATE = """You are a rating prediction system. Based on the review text below, predict the star rating (1-5).

Review: "{review_text}"

Return ONLY a JSON object in this exact format:
{{"predicted_stars": <number>, "explanation": "<brief reason>"}}"""

# Groq-based predict_rating function
def predict_rating(review_text, prompt_template, max_retries=2):
    """Call Groq API and return parsed JSON response"""
    prompt = prompt_template.format(review_text=review_text)
    
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.1,  # Low temperature for consistent predictions
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            
            print(f"\n--- Raw Response (Attempt {attempt + 1}) ---")
            print(response_text[:200] + "..." if len(response_text) > 200 else response_text)
            
            # Clean up markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            result = json.loads(response_text)
    
            if "predicted_stars" in result and "explanation" in result:
                return {
                    "predicted_stars": int(result["predicted_stars"]),
                    "explanation": result["explanation"],
                    "is_valid": True,
                    "raw_response": response_text
                }
            else:
                return {"is_valid": False, "error": "Missing required fields", "raw_response": response_text}
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {str(e)}")
            if attempt == max_retries - 1:
                return {"is_valid": False, "error": f"JSON parse error: {str(e)}", "raw_response": response_text}
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            if attempt == max_retries - 1:
                return {"is_valid": False, "error": str(e), "raw_response": str(e)}
        
        time.sleep(0.5)  # Short wait before retry
    
    return {"is_valid": False, "error": "Max retries exceeded"}


# Test the function
print("\n" + "="*70)
print("TESTING GROQ-BASED PREDICT_RATING FUNCTION")
print("="*70)

valid_count = 0
results = []

for idx, row in df_test.iterrows():
    print(f"\n{'='*70}")
    print(f"Test {idx + 1}/5")
    print(f"{'='*70}")
    print(f"Review: {row['text'][:100]}...")
    print(f"Actual Stars: {row['stars']}")
    
    result = predict_rating(row['text'], PROMPT_TEMPLATE)
    results.append(result)
    
    if result['is_valid']:
        valid_count += 1
        print(f"✓ VALID - Predicted: {result['predicted_stars']} stars")
        print(f"  Explanation: {result['explanation'][:100]}...")
    else:
        print(f"❌ INVALID - Error: {result.get('error', 'Unknown error')}")
    
    time.sleep(0.2)  # Groq has better rate limits

# Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)
print(f"Valid JSON responses: {valid_count}/5")
print(f"Success rate: {valid_count/5*100:.1f}%")

if valid_count >= 4:
    print("\n✅ SUCCESS! Groq is working correctly.")
    print("You can now run the full evaluation with 200 reviews.")
    print("Estimated time: ~2-3 minutes (much faster than Gemini!)")
elif valid_count >= 2:
    print("\n⚠️  PARTIAL SUCCESS. Some responses failed.")
    print("Check the error messages above to debug further.")
else:
    print("\n❌ FAILED. Most responses are invalid.")
    print("Check your GROQ_API_KEY in .env file.")

# Show sample results
print("\n" + "="*70)
print("SAMPLE RESULTS")
print("="*70)
for i, result in enumerate(results[:3], 1):
    print(f"\nResult {i}:")
    print(json.dumps(result, indent=2))
