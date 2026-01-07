def predict_rating(review_text, prompt_template, max_retries=2):
    """Call Gemini API and return parsed JSON response"""
    prompt = prompt_template.format(review_text=review_text)
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            response_text = response.text.strip()
            
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
            if attempt == max_retries - 1:
                return {"is_valid": False, "error": f"JSON parse error: {str(e)}", "raw_response": response_text}
        except Exception as e:
            if attempt == max_retries - 1:
                return {"is_valid": False, "error": str(e), "raw_response": str(e)}
        
        time.sleep(1)  # Wait before retry
    
    return {"is_valid": False, "error": "Max retries exceeded"}
