"""
Full evaluation script using Groq API
Evaluates 3 prompts on 200 Yelp reviews
Much faster than Gemini - estimated time: 5-10 minutes
"""

import os
from groq import Groq
import pandas as pd
import json
import time
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Initialize Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
print("✓ Groq client initialized")
print("✓ Using model: llama-3.3-70b-versatile")

# Load data
df = pd.read_csv('yelp.csv')
df_sample = df.sample(n=200, random_state=42).reset_index(drop=True)
print(f"✓ Loaded {len(df_sample)} reviews for evaluation")

# Define prompts
PROMPT_1_TEMPLATE = """You are a rating prediction system. Based on the review text below, predict the star rating (1-5).

Review: "{review_text}"

Return ONLY a JSON object in this exact format:
{{"predicted_stars": <number>, "explanation": "<brief reason>"}}"""

PROMPT_2_TEMPLATE = """Analyze the following review step-by-step:

Review: "{review_text}"

Steps:
1. Identify the sentiment (positive, negative, neutral, mixed)
2. Look for specific indicators (complaints, praise, specific issues, enthusiasm level)
3. Based on these factors, determine the star rating (1-5)

Return ONLY a JSON object:
{{"predicted_stars": <number>, "explanation": "<reasoning based on sentiment and indicators>"}}"""

PROMPT_3_TEMPLATE = """You are an expert at predicting star ratings from reviews. Here are examples:

Example 1:
Review: "Absolutely amazing food! Best pizza I've ever had. Service was fantastic too."
Output: {{"predicted_stars": 5, "explanation": "Highly positive language with superlatives indicating excellent experience"}}

Example 2:
Review: "Food was okay, nothing special. Service took forever."
Output: {{"predicted_stars": 2, "explanation": "Mediocre food quality combined with poor service indicates below average experience"}}

Example 3:
Review: "Good food and decent prices. Could be better but satisfied overall."
Output: {{"predicted_stars": 4, "explanation": "Positive with minor reservations suggests good but not perfect experience"}}

Now predict for this review:
Review: "{review_text}"

Return ONLY a JSON object:
{{"predicted_stars": <number>, "explanation": "<brief reasoning>"}}"""

prompts = {
    "Prompt 1 (Basic)": PROMPT_1_TEMPLATE,
    "Prompt 2 (Chain-of-Thought)": PROMPT_2_TEMPLATE,
    "Prompt 3 (Few-Shot)": PROMPT_3_TEMPLATE
}

# Prediction function
def predict_rating(review_text, prompt_template, max_retries=2):
    """Call Groq API and return parsed JSON response"""
    prompt = prompt_template.format(review_text=review_text)
    
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            
            # Clean up markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
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
            if attempt == max_retries - 1:
                return {"is_valid": False, "error": f"JSON parse error: {str(e)}", "raw_response": response_text}
        except Exception as e:
            if attempt == max_retries - 1:
                return {"is_valid": False, "error": str(e), "raw_response": str(e)}
        
        time.sleep(0.3)
    
    return {"is_valid": False, "error": "Max retries exceeded"}

# Metrics functions
def calculate_metrics(predictions):
    valid_predictions = [p for p in predictions if p['is_valid']]
    
    if not valid_predictions:
        return {
            'accuracy': 0,
            'valid_count': 0,
            'total_count': len(predictions),
            'json_validity_rate': 0
        }
    
    actual = [p['actual_stars'] for p in valid_predictions]
    predicted = [p['predicted_stars'] for p in valid_predictions]
    
    accuracy = accuracy_score(actual, predicted)
    conf_matrix = confusion_matrix(actual, predicted, labels=[1, 2, 3, 4, 5])
    
    return {
        'accuracy': accuracy,
        'valid_count': len(valid_predictions),
        'total_count': len(predictions),
        'json_validity_rate': len(valid_predictions) / len(predictions),
        'confusion_matrix': conf_matrix,
        'actual': actual,
        'predicted': predicted
    }

def calculate_consistency(predictions):
    valid_predictions = [p for p in predictions if p['is_valid']]
    if not valid_predictions:
        return 0
    
    errors = [abs(p['predicted_stars'] - p['actual_stars']) for p in valid_predictions]
    return np.std(errors)

# Run evaluation
results = {}

for prompt_name, prompt_template in prompts.items():
    print(f"\n{'='*60}")
    print(f"Testing: {prompt_name}")
    print(f"{'='*60}")
    
    predictions = []
    valid_count = 0
    
    for idx, row in df_sample.iterrows():
        result = predict_rating(row['text'], prompt_template)
        result['actual_stars'] = row['stars']
        predictions.append(result)
        
        if result['is_valid']:
            valid_count += 1
        
        if (idx + 1) % 20 == 0:
            print(f"Processed {idx + 1}/{len(df_sample)} reviews...")
        
        time.sleep(0.1)  # Groq rate limiting (very generous)
    
    results[prompt_name] = predictions
    print(f"Completed! Valid JSON responses: {valid_count}/{len(df_sample)}")

# Calculate and display metrics
print("\n" + "="*70)
print("RESULTS SUMMARY")
print("="*70)

metrics_summary = {}

for prompt_name, predictions in results.items():
    metrics = calculate_metrics(predictions)
    consistency = calculate_consistency(predictions)
    
    metrics_summary[prompt_name] = {
        'Accuracy': f"{metrics['accuracy']:.2%}",
        'JSON Validity Rate': f"{metrics['json_validity_rate']:.2%}",
        'Valid Predictions': f"{metrics['valid_count']}/{metrics['total_count']}",
        'Consistency (Lower is Better)': f"{consistency:.3f}"
    }
    
    print(f"\n{prompt_name}:")
    print(f"  Accuracy: {metrics['accuracy']:.2%}")
    print(f"  JSON Validity: {metrics['json_validity_rate']:.2%}")
    print(f"  Valid Predictions: {metrics['valid_count']}/{metrics['total_count']}")
    print(f"  Consistency: {consistency:.3f}")

# Save results
comparison_df = pd.DataFrame(metrics_summary).T
print("\n" + "="*70)
print("COMPARISON TABLE")
print("="*70)
print(comparison_df.to_string())

comparison_df.to_csv('prompt_comparison_results.csv')
print("\n✓ Results saved to 'prompt_comparison_results.csv'")

# Save detailed predictions
with open('detailed_predictions.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
print("✓ Detailed predictions saved to 'detailed_predictions.json'")

print("\n" + "="*70)
print("EVALUATION COMPLETE!")
print("="*70)
