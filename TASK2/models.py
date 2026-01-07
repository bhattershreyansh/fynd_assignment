from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# Request Models
class ReviewSubmitRequest(BaseModel):
    """Request model for submitting a review"""
    name: str = Field(..., min_length=1, max_length=50, description="Customer name")
    rating: int = Field(..., ge=1, le=5, description="Star rating from 1 to 5")
    review_text: str = Field(..., min_length=10, max_length=5000, description="Review text")
    
    @field_validator('review_text')
    @classmethod
    def validate_review_text(cls, v: str) -> str:
        """Validate review text is not just whitespace"""
        if not v.strip():
            raise ValueError("Review text cannot be empty or just whitespace")
        return v.strip()


# Response Models
class ReviewSubmitResponse(BaseModel):
    """Response model after submitting a review"""
    id: str
    rating: int
    review_text: str
    user_response: str
    created_at: datetime
    status: str = "success"
    
    class Config:
        from_attributes = True


class AdminReviewItem(BaseModel):
    """Single review item for admin dashboard"""
    id: str
    rating: int
    review_text: str
    summary: Optional[str] = None
    recommended_actions: Optional[List[str]] = None
    user_response: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AdminReviewsResponse(BaseModel):
    """Response model for admin reviews list"""
    reviews: List[AdminReviewItem]
    total: int
    page: int
    page_size: int


class AnalyticsResponse(BaseModel):
    """Response model for analytics"""
    total_reviews: int
    average_rating: float
    rating_distribution: dict[int, int]  # {1: 10, 2: 5, 3: 20, 4: 30, 5: 35}
    recent_reviews_count: int  # Last 24 hours


class PriorityReviewsResponse(BaseModel):
    """Response model for priority/urgent reviews"""
    urgent_reviews: List[AdminReviewItem]
    total_urgent: int
    message: str = "Reviews requiring immediate attention"


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status: str = "error"
