from google import genai
import os
from dotenv import load_dotenv
import time
from typing import Tuple, List, Optional
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=GEMINI_API_KEY)


class AIService:
    """Service for AI-powered review analysis"""
    
    def __init__(self):
        self.model = "gemini-2.5-flash"
        self.max_retries = 2
    
    def _call_llm(self, prompt: str, retry_count: int = 0) -> Optional[str]:
        """Call LLM with retry logic"""
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"LLM call failed (attempt {retry_count + 1}): {str(e)}")
            if retry_count < self.max_retries:
                time.sleep(1)
                return self._call_llm(prompt, retry_count + 1)
            return None
    
    def generate_user_response(self, name: str, rating: int, review_text: str) -> str:
        """Generate a personalized response for the user"""
        prompt = f"""You are a customer service representative. A customer named {name} has left a {rating}-star review.

Review: "{review_text}"

Generate a warm, professional, and personalized response (2-3 sentences) that:
1. Addresses them by name
2. Thanks them for their feedback
3. Addresses their specific points
4. Is appropriate for a {rating}-star rating

Response:"""
        
        response = self._call_llm(prompt)
        
        # Fallback responses if LLM fails
        if not response:
            fallback_responses = {
                5: "Thank you so much for your wonderful 5-star review! We're thrilled to hear about your positive experience.",
                4: "Thank you for your 4-star review! We appreciate your feedback and are glad you had a good experience.",
                3: "Thank you for your review. We appreciate your feedback and will work to improve your experience.",
                2: "Thank you for sharing your feedback. We're sorry your experience wasn't better and will work to address your concerns.",
                1: "We sincerely apologize for your experience. Your feedback is important to us and we will take immediate action to improve."
            }
            return fallback_responses.get(rating, "Thank you for your feedback!")
        
        return response
    
    def generate_summary(self, review_text: str) -> str:
        """Generate a concise summary of the review"""
        prompt = f"""Summarize this customer review in one concise sentence (max 15 words):

Review: "{review_text}"

Summary:"""
        
        response = self._call_llm(prompt)
        
        # Fallback if LLM fails
        if not response:
            # Simple truncation fallback
            return review_text[:100] + "..." if len(review_text) > 100 else review_text
        
        return response
    
    def generate_recommended_actions(self, rating: int, review_text: str) -> List[str]:
        """Generate recommended actions for admin"""
        prompt = f"""Based on this {rating}-star review, suggest 2-3 specific, actionable next steps for the business.

Review: "{review_text}"

Provide ONLY the action items as a numbered list:"""
        
        response = self._call_llm(prompt)
        
        # Fallback actions if LLM fails
        if not response:
            fallback_actions = {
                5: ["Send thank you message", "Request testimonial", "Offer loyalty reward"],
                4: ["Follow up on feedback", "Identify improvement areas"],
                3: ["Investigate concerns", "Follow up with customer", "Review service quality"],
                2: ["Contact customer immediately", "Investigate issues", "Offer compensation"],
                1: ["Urgent: Contact customer", "Escalate to management", "Conduct internal review"]
            }
            return fallback_actions.get(rating, ["Review feedback", "Take appropriate action"])
        
        # Parse numbered list
        actions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering/bullets
                clean_line = line.lstrip('0123456789.-•) ').strip()
                # Remove markdown formatting (**, __, etc.)
                clean_line = clean_line.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
                if clean_line:
                    actions.append(clean_line)
        
        return actions[:3] if actions else ["Review feedback", "Take appropriate action"]
    
    def process_review(self, name: str, rating: int, review_text: str) -> Tuple[str, str, List[str]]:
        """
        Process a review and generate all AI outputs
        Returns: (user_response, summary, recommended_actions)
        """
        logger.info(f"Processing review from {name} with rating {rating}")
        
        # Generate all three AI outputs
        user_response = self.generate_user_response(name, rating, review_text)
        summary = self.generate_summary(review_text)
        recommended_actions = self.generate_recommended_actions(rating, review_text)
        
        logger.info("Review processing completed")
        
        return user_response, summary, recommended_actions


# Singleton instance
ai_service = AIService()
