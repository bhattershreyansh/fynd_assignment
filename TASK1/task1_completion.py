# ============================================================================
# MISSING CODE TO ADD TO YOUR NOTEBOOK
# Copy these cells into task1.ipynb in the appropriate locations
# ============================================================================

# ============================================================================
# CELL 1: Model Initialization (Add after API key cell)
# ============================================================================
"""
# Initialize Gemini model using latest SDK
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)
print("✓ Gemini client initialized successfully!")
print("✓ Using model: gemini-2.5-flash")
"""

# ============================================================================
# CELL 2: Evaluation Functions (Add after predict_rating function)
# ============================================================================
"""
def calculate_metrics(predictions):
    '''Calculate accuracy and other metrics from predictions'''
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
    '''Calculate prediction consistency (std dev of errors)'''
    valid_predictions = [p for p in predictions if p['is_valid']]
    if not valid_predictions:
        return 0
    
    errors = [abs(p['predicted_stars'] - p['actual_stars']) for p in valid_predictions]
    return np.std(errors)
"""

# ============================================================================
# CELL 3: Run Evaluation (Add after the testing loop)
# ============================================================================
"""
# Calculate metrics for each prompt
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
    
    print(f"\n{'='*60}")
    print(f"{prompt_name} - Results")
    print(f"{'='*60}")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"JSON Validity: {metrics['json_validity_rate']:.2%}")
    print(f"Valid Predictions: {metrics['valid_count']}/{metrics['total_count']}")
    print(f"Consistency (Std Dev of Errors): {consistency:.3f}")
"""

# ============================================================================
# CELL 4: Comparison Table (Add after metrics calculation)
# ============================================================================
"""
# Create comparison DataFrame
comparison_df = pd.DataFrame(metrics_summary).T
print("\n" + "="*80)
print("COMPARISON TABLE - All Prompts")
print("="*80)
print(comparison_df.to_string())
print("\n")

# Save results
comparison_df.to_csv('prompt_comparison_results.csv')
print("Results saved to 'prompt_comparison_results.csv'")
"""

# ============================================================================
# CELL 5: Visualizations (Add after comparison table)
# ============================================================================
"""
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Accuracy Comparison
prompt_names = list(metrics_summary.keys())
accuracies = [float(metrics_summary[p]['Accuracy'].strip('%'))/100 for p in prompt_names]
axes[0, 0].bar(range(len(prompt_names)), accuracies, color=['#3498db', '#e74c3c', '#2ecc71'])
axes[0, 0].set_xticks(range(len(prompt_names)))
axes[0, 0].set_xticklabels(prompt_names, rotation=15, ha='right')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].set_title('Accuracy Comparison Across Prompts')
axes[0, 0].set_ylim([0, 1])
for i, v in enumerate(accuracies):
    axes[0, 0].text(i, v + 0.02, f'{v:.2%}', ha='center', va='bottom', fontweight='bold')

# 2. JSON Validity Rate
validity_rates = [float(metrics_summary[p]['JSON Validity Rate'].strip('%'))/100 for p in prompt_names]
axes[0, 1].bar(range(len(prompt_names)), validity_rates, color=['#9b59b6', '#f39c12', '#1abc9c'])
axes[0, 1].set_xticks(range(len(prompt_names)))
axes[0, 1].set_xticklabels(prompt_names, rotation=15, ha='right')
axes[0, 1].set_ylabel('JSON Validity Rate')
axes[0, 1].set_title('JSON Validity Rate Comparison')
axes[0, 1].set_ylim([0, 1])
for i, v in enumerate(validity_rates):
    axes[0, 1].text(i, v + 0.02, f'{v:.2%}', ha='center', va='bottom', fontweight='bold')

# 3. Confusion Matrix for Best Performing Prompt
best_prompt = max(metrics_summary.keys(), key=lambda x: float(metrics_summary[x]['Accuracy'].strip('%')))
best_metrics = calculate_metrics(results[best_prompt])
sns.heatmap(best_metrics['confusion_matrix'], annot=True, fmt='d', cmap='Blues', 
            xticklabels=[1,2,3,4,5], yticklabels=[1,2,3,4,5], ax=axes[1, 0])
axes[1, 0].set_xlabel('Predicted Stars')
axes[1, 0].set_ylabel('Actual Stars')
axes[1, 0].set_title(f'Confusion Matrix - {best_prompt}')

# 4. Error Distribution
all_errors = []
all_labels = []
for prompt_name in prompt_names:
    valid_preds = [p for p in results[prompt_name] if p['is_valid']]
    errors = [abs(p['predicted_stars'] - p['actual_stars']) for p in valid_preds]
    all_errors.extend(errors)
    all_labels.extend([prompt_name] * len(errors))

error_df = pd.DataFrame({'Prompt': all_labels, 'Absolute Error': all_errors})
sns.boxplot(data=error_df, x='Prompt', y='Absolute Error', ax=axes[1, 1])
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=15, ha='right')
axes[1, 1].set_title('Error Distribution Across Prompts')

plt.tight_layout()
plt.savefig('prompt_evaluation_results.png', dpi=300, bbox_inches='tight')
plt.show()

print("Visualization saved to 'prompt_evaluation_results.png'")
"""

# ============================================================================
# CELL 6: Detailed Analysis and Discussion (Add at the end)
# ============================================================================
"""
print("\n" + "="*80)
print("DETAILED ANALYSIS & DISCUSSION")
print("="*80)

print("\n### PROMPT DESIGN RATIONALE ###\n")

print("1. PROMPT 1 (Basic):")
print("   - Simple, direct instruction")
print("   - Minimal guidance to the model")
print("   - Tests baseline performance")
print("   - Expected: Fast but potentially less accurate")

print("\n2. PROMPT 2 (Chain-of-Thought):")
print("   - Guides model through reasoning steps")
print("   - Explicitly asks to identify sentiment and indicators")
print("   - Expected: Better reasoning, potentially higher accuracy")
print("   - Trade-off: Slightly longer processing time")

print("\n3. PROMPT 3 (Few-Shot):")
print("   - Provides concrete examples of rating patterns")
print("   - Shows model what good predictions look like")
print("   - Expected: Most consistent and accurate")
print("   - Trade-off: Longer prompt = higher token usage")

print("\n### RESULTS SUMMARY ###\n")

# Find best performing prompt for each metric
best_accuracy = max(metrics_summary.keys(), key=lambda x: float(metrics_summary[x]['Accuracy'].strip('%')))
best_validity = max(metrics_summary.keys(), key=lambda x: float(metrics_summary[x]['JSON Validity Rate'].strip('%')))
best_consistency = min(metrics_summary.keys(), key=lambda x: float(metrics_summary[x]['Consistency (Lower is Better)']))

print(f"Best Accuracy: {best_accuracy} ({metrics_summary[best_accuracy]['Accuracy']})")
print(f"Best JSON Validity: {best_validity} ({metrics_summary[best_validity]['JSON Validity Rate']})")
print(f"Best Consistency: {best_consistency} ({metrics_summary[best_consistency]['Consistency (Lower is Better)']})")

print("\n### KEY FINDINGS ###\n")
print("1. Accuracy: How well each prompt predicted the correct star rating")
print("2. JSON Validity: How reliably each prompt returned properly formatted JSON")
print("3. Consistency: How stable the predictions are (lower std dev = more reliable)")

print("\n### TRADE-OFFS ###\n")
print("- Basic Prompt: Fast, simple, but may lack nuance")
print("- Chain-of-Thought: Better reasoning, but requires more tokens")
print("- Few-Shot: Most accurate, but highest token cost and prompt complexity")

print("\n### RECOMMENDATIONS ###\n")
if best_accuracy == best_validity == best_consistency:
    print(f"✓ {best_accuracy} is the clear winner across all metrics")
else:
    print("✓ Choose based on priority:")
    print(f"  - For accuracy: {best_accuracy}")
    print(f"  - For reliability: {best_validity}")
    print(f"  - For consistency: {best_consistency}")
"""

# ============================================================================
# CELL 7: Save All Results (Add at the very end)
# ============================================================================
"""
# Save detailed predictions to JSON
import json

with open('detailed_predictions.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\nAll results saved!")
print("- prompt_comparison_results.csv")
print("- prompt_evaluation_results.png")
print("- detailed_predictions.json")
"""
