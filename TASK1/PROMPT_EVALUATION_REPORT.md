# Prompt Engineering Evaluation Report
## Yelp Review Star Rating Prediction

**Author:** Shreyansh Bhatter  
**Date:** January 7, 2026  
**Model:** Groq API - llama-3.3-70b-versatile  
**Dataset:** 100 Yelp reviews (sampled from yelp.csv)

---

## Executive Summary

This report evaluates three different prompt engineering strategies for predicting star ratings (1-5) from Yelp review text. The evaluation focuses on accuracy, reliability (JSON validity), and consistency across 100 sampled reviews.

**Key Finding:** Prompt 1 (Basic) is recommended for production use due to its 100% reliability and strong performance, despite Prompt 3 achieving slightly higher accuracy.

---

## Prompt Versions

### Prompt 1: Basic Approach

**Design Philosophy:** Simple, direct instruction with minimal guidance.

```
You are a rating prediction system. Based on the review text below, 
predict the star rating (1-5).

Review: "{review_text}"

Return ONLY a JSON object in this exact format:
{"predicted_stars": <number>, "explanation": "<brief reason>"}
```

**Rationale:**
- Tests baseline performance with minimal prompt engineering
- Clear, concise instructions reduce model confusion
- Explicit JSON format specification ensures structured output
- Fast processing due to short prompt length

**Expected Outcome:** Fast execution, high reliability, potentially less nuanced predictions

---

### Prompt 2: Chain-of-Thought Approach

**Design Philosophy:** Guide the model through explicit reasoning steps.

```
Analyze the following review step-by-step:

Review: "{review_text}"

Steps:
1. Identify the sentiment (positive, negative, neutral, mixed)
2. Look for specific indicators (complaints, praise, specific issues, enthusiasm level)
3. Based on these factors, determine the star rating (1-5)

Return ONLY a JSON object:
{"predicted_stars": <number>, "explanation": "<reasoning based on sentiment and indicators>"}
```

**Rationale:**
- Explicitly asks model to identify sentiment before rating
- Breaks down the task into logical steps
- Encourages deeper analysis of review content
- May improve reasoning quality and explanation clarity

**Expected Outcome:** Better reasoning process, potentially higher accuracy, slightly longer processing time

**Improvement from Prompt 1:** Added structured thinking process to improve decision quality

---

### Prompt 3: Few-Shot Learning Approach

**Design Philosophy:** Provide concrete examples to demonstrate desired behavior.

```
You are an expert at predicting star ratings from reviews. Here are examples:

Example 1:
Review: "Absolutely amazing food! Best pizza I've ever had. Service was fantastic too."
Output: {"predicted_stars": 5, "explanation": "Highly positive language with superlatives indicating excellent experience"}

Example 2:
Review: "Food was okay, nothing special. Service took forever."
Output: {"predicted_stars": 2, "explanation": "Mediocre food quality combined with poor service indicates below average experience"}

Example 3:
Review: "Good food and decent prices. Could be better but satisfied overall."
Output: {"predicted_stars": 4, "explanation": "Positive with minor reservations suggests good but not perfect experience"}

Now predict for this review:
Review: "{review_text}"

Return ONLY a JSON object:
{"predicted_stars": <number>, "explanation": "<brief reasoning>"}
```

**Rationale:**
- Shows model concrete examples of rating patterns
- Demonstrates how to map sentiment to star ratings
- Provides template for explanation quality
- Covers range of ratings (2, 4, 5) to show variety

**Expected Outcome:** Most accurate predictions, highest token usage, potential for format inconsistency

**Improvement from Prompts 1 & 2:** Added learning-by-example to improve pattern recognition

---

## Evaluation Methodology

### Dataset
- **Source:** Yelp review dataset (yelp.csv)
- **Sample Size:** 100 reviews
- **Sampling Method:** Random sampling with seed=42 for reproducibility
- **Features Used:** Review text and actual star rating

### Metrics

1. **Accuracy:** Percentage of predictions where predicted stars exactly match actual stars
   - Formula: `(Correct Predictions / Total Valid Predictions) × 100`
   - Only exact matches count (predicted=4, actual=4 ✓)

2. **JSON Validity Rate:** Percentage of responses that returned valid, parseable JSON
   - Formula: `(Valid JSON Responses / Total Attempts) × 100`
   - Critical for production reliability

3. **Consistency:** Standard deviation of prediction errors
   - Formula: `std_dev(|predicted - actual|)`
   - Lower values indicate more stable predictions

### Testing Environment
- **API:** Groq (llama-3.3-70b-versatile)
- **Temperature:** 0.1 (low for consistent predictions)
- **Max Retries:** 2 per prediction
- **Rate Limiting:** 0.1s delay between requests

---

## Results

### Comparison Table

| Metric | Prompt 1 (Basic) | Prompt 2 (Chain-of-Thought) | Prompt 3 (Few-Shot) |
|--------|------------------|----------------------------|---------------------|
| **Accuracy** | 62.00% | 59.00% | **63.51%** ⭐ |
| **JSON Validity Rate** | **100.00%** ⭐ | **100.00%** ⭐ | 74.00% |
| **Valid Predictions** | 100/100 | 100/100 | 74/100 |
| **Consistency (Std Dev)** | **0.508** ⭐ | 0.534 | 0.512 |
| **Processing Speed** | Fast | Medium | Slower |
| **Token Usage** | Low | Medium | High |

⭐ = Best performance in category

### Detailed Performance Analysis

#### Prompt 1 (Basic)
- ✅ **Perfect reliability:** 100% JSON validity
- ✅ **Best consistency:** Lowest error variance (0.508)
- ✅ **Strong accuracy:** 62% correct predictions
- ✅ **Fastest execution:** Minimal prompt overhead
- ⚠️ **Slightly lower accuracy** than Prompt 3 (1.5% difference)

#### Prompt 2 (Chain-of-Thought)
- ✅ **Perfect reliability:** 100% JSON validity
- ✅ **Good explanations:** Reasoning steps visible in responses
- ⚠️ **Lowest accuracy:** 59% correct predictions
- ⚠️ **Moderate consistency:** Highest error variance (0.534)
- 💡 **Insight:** Explicit reasoning didn't improve accuracy as expected

#### Prompt 3 (Few-Shot)
- ✅ **Highest accuracy:** 63.51% when it works
- ❌ **Poor reliability:** Only 74% JSON validity
- ❌ **26 failed responses:** Lost predictions due to format errors
- ⚠️ **High token cost:** Longest prompt = highest API costs
- 💡 **Insight:** Examples help but introduce complexity

---

## Discussion of Results

### Key Findings

1. **Reliability vs. Accuracy Trade-off**
   - Prompt 3 achieved highest accuracy (63.51%) but lowest reliability (74%)
   - Prompt 1 balanced strong accuracy (62%) with perfect reliability (100%)
   - The 1.5% accuracy gain from Prompt 3 comes at the cost of 26% failed responses

2. **Chain-of-Thought Underperformed**
   - Despite explicit reasoning steps, Prompt 2 had the lowest accuracy (59%)
   - This suggests that for this task, structured thinking may overcomplicate the model's decision process
   - The model may perform better with direct instructions

3. **Consistency Matters**
   - Prompt 1 had the lowest error variance (0.508)
   - More consistent predictions are valuable for production systems
   - Predictable behavior is easier to debug and improve

### Why Prompt 3 Had Lower JSON Validity

The few-shot prompt's 74% JSON validity rate is explained by:

1. **Prompt Complexity:** Longer prompts with multiple examples can confuse the model
2. **Format Confusion:** Model may try to mimic example structure too closely
3. **Token Limits:** Less room for response with longer input
4. **Creative Responses:** Examples may encourage additional commentary outside JSON

### Trade-offs Analysis

| Aspect | Prompt 1 | Prompt 2 | Prompt 3 |
|--------|----------|----------|----------|
| **Simplicity** | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **Reliability** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| **Accuracy** | ⭐⭐ | ⭐ | ⭐⭐⭐ |
| **Cost Efficiency** | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **Maintainability** | ⭐⭐⭐ | ⭐⭐ | ⭐ |

---

## Recommendations

### For Production Use: **Prompt 1 (Basic)** ✅

**Reasoning:**
1. **100% Reliability:** No failed responses ensures consistent user experience
2. **Strong Performance:** 62% accuracy is only 1.5% below the highest
3. **Cost Effective:** Minimal token usage reduces API costs
4. **Easy to Maintain:** Simple prompts are easier to debug and improve
5. **Predictable Behavior:** Lowest error variance means stable predictions

### When to Use Other Prompts

**Prompt 2 (Chain-of-Thought):**
- When detailed explanations are more important than accuracy
- When debugging model reasoning is required
- When transparency in decision-making is critical

**Prompt 3 (Few-Shot):**
- When maximum accuracy is critical and failures are acceptable
- When you can implement robust error handling for failed responses
- When API costs are not a concern
- After improving the prompt to increase JSON validity

---

## Potential Improvements

### For Prompt 3 (Few-Shot)
To improve JSON validity while maintaining accuracy:

1. **Stricter Instructions:** Add "Return ONLY a JSON object, absolutely nothing else"
2. **Simplify Examples:** Use shorter review texts in examples
3. **Reduce Examples:** Test with 2 examples instead of 3
4. **Add JSON Schema:** Explicitly show the exact format expected
5. **Post-Processing:** Implement robust JSON extraction from responses

### For All Prompts
1. **Increase Sample Size:** Test on 200+ reviews for more statistical significance
2. **Error Analysis:** Examine misclassified reviews to identify patterns
3. **A/B Testing:** Test prompts on different review categories (food, service, etc.)
4. **Hybrid Approach:** Combine best elements from multiple prompts

---

## Conclusion

This evaluation demonstrates that **simpler is often better** in prompt engineering. While sophisticated techniques like few-shot learning can improve accuracy, they introduce complexity that may reduce reliability.

**Prompt 1 (Basic)** strikes the optimal balance between:
- Performance (62% accuracy)
- Reliability (100% JSON validity)
- Consistency (0.508 error std dev)
- Cost efficiency (minimal tokens)

For a production system predicting Yelp review ratings, **Prompt 1 is the recommended choice**. The marginal accuracy gain from more complex prompts does not justify the loss in reliability and increased costs.

---

## Appendix

### Files Generated
- `prompt_comparison_results.csv` - Numerical comparison of all metrics
- `prompt_evaluation_results.png` - Visual comparison charts (4 subplots)
- `detailed_predictions.json` - Full prediction data for all prompts
- `task1_groq.ipynb` - Complete evaluation notebook with code

### Reproducibility
- Random seed: 42
- Model: llama-3.3-70b-versatile
- Temperature: 0.1
- Sample size: 100 reviews
- Date: January 7, 2026
