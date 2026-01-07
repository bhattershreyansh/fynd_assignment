from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import uuid
import logging
import csv
import io

from models import (
    ReviewSubmitRequest,
    ReviewSubmitResponse,
    AdminReviewsResponse,
    AdminReviewItem,
    AnalyticsResponse,
    PriorityReviewsResponse,
    ErrorResponse
)
from database import get_db, init_db, Review
from ai_service import ai_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Review System API",
    description="Backend API for review submission and admin dashboard",
    version="1.0.0"
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")


# Health check endpoint
@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "Review System API",
        "version": "1.0.0"
    }


# Submit review endpoint (User-facing)
@app.post("/api/reviews", response_model=ReviewSubmitResponse, responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
def submit_review(
    review_request: ReviewSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Submit a new review (User-facing endpoint)
    
    - **rating**: Star rating from 1 to 5
    - **review_text**: Review text (10-5000 characters)
    
    Returns AI-generated response for the user
    """
    try:
        logger.info(f"Received review submission: rating={review_request.rating}")
        
        # Generate AI responses (server-side)
        user_response, summary, recommended_actions = ai_service.process_review(
            review_request.rating,
            review_request.review_text
        )
        
        # Create review record
        review_id = str(uuid.uuid4())
        db_review = Review(
            id=review_id,
            rating=review_request.rating,
            review_text=review_request.review_text,
            summary=summary,
            recommended_actions=recommended_actions,
            user_response=user_response,
            created_at=datetime.utcnow()
        )
        
        # Save to database
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        logger.info(f"Review saved successfully: id={review_id}")
        
        # Return response to user
        return ReviewSubmitResponse(
            id=db_review.id,
            rating=db_review.rating,
            review_text=db_review.review_text,
            user_response=db_review.user_response,
            created_at=db_review.created_at,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Error submitting review: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit review: {str(e)}")


# Get all reviews endpoint (Admin-facing)
@app.get("/api/reviews", response_model=AdminReviewsResponse)
def get_reviews(
    rating: int = Query(None, ge=1, le=5, description="Filter by rating"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all reviews (Admin-facing endpoint)
    
    - **rating**: Optional filter by star rating
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 50, max: 100)
    
    Returns list of reviews with AI-generated summaries and recommended actions
    """
    try:
        # Build query
        query = db.query(Review)
        
        # Apply rating filter if provided
        if rating is not None:
            query = query.filter(Review.rating == rating)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        reviews = query.order_by(desc(Review.created_at)).offset((page - 1) * page_size).limit(page_size).all()
        
        # Convert to response model
        review_items = [
            AdminReviewItem(
                id=review.id,
                rating=review.rating,
                review_text=review.review_text,
                summary=review.summary,
                recommended_actions=review.recommended_actions,
                user_response=review.user_response,
                created_at=review.created_at
            )
            for review in reviews
        ]
        
        return AdminReviewsResponse(
            reviews=review_items,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Error fetching reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")



# Analytics endpoint (Admin-facing)
@app.get("/api/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """
    Get analytics and statistics (Admin-facing endpoint)
    
    Returns:
    - Total reviews count
    - Average rating
    - Rating distribution
    - Recent reviews count (last 24 hours)
    """
    try:
        # Total reviews
        total_reviews = db.query(Review).count()
        
        # Average rating
        avg_rating = db.query(func.avg(Review.rating)).scalar() or 0.0
        
        # Rating distribution
        rating_distribution = {}
        for rating in range(1, 6):
            count = db.query(Review).filter(Review.rating == rating).count()
            rating_distribution[rating] = count
        
        # Recent reviews (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_count = db.query(Review).filter(Review.created_at >= yesterday).count()
        
        return AnalyticsResponse(
            total_reviews=total_reviews,
            average_rating=round(avg_rating, 2),
            rating_distribution=rating_distribution,
            recent_reviews_count=recent_count
        )
        
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")


# Priority reviews endpoint (Admin-facing) - MUST come before /{review_id}
@app.get("/api/reviews/priority", response_model=PriorityReviewsResponse)
def get_priority_reviews(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of urgent reviews to return"),
    db: Session = Depends(get_db)
):
    """
    Get priority/urgent reviews (1-2 star ratings) (Admin-facing endpoint)
    
    - **limit**: Maximum number of urgent reviews to return (default: 20, max: 100)
    
    Returns reviews that need immediate attention, sorted by most recent first
    """
    try:
        # Query for 1-2 star reviews
        urgent_reviews = db.query(Review).filter(
            Review.rating.in_([1, 2])
        ).order_by(desc(Review.created_at)).limit(limit).all()
        
        total_urgent = db.query(Review).filter(Review.rating.in_([1, 2])).count()
        
        # Convert to response model
        review_items = [
            AdminReviewItem(
                id=review.id,
                rating=review.rating,
                review_text=review.review_text,
                summary=review.summary,
                recommended_actions=review.recommended_actions,
                user_response=review.user_response,
                created_at=review.created_at
            )
            for review in urgent_reviews
        ]
        
        return PriorityReviewsResponse(
            urgent_reviews=review_items,
            total_urgent=total_urgent,
            message=f"Found {total_urgent} reviews requiring immediate attention"
        )
        
    except Exception as e:
        logger.error(f"Error fetching priority reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch priority reviews: {str(e)}")


# Export reviews to CSV endpoint (Admin-facing) - MUST come before /{review_id}
@app.get("/api/reviews/export")
def export_reviews(
    rating: int = Query(None, ge=1, le=5, description="Filter by rating"),
    db: Session = Depends(get_db)
):
    """
    Export reviews to CSV (Admin-facing endpoint)
    
    - **rating**: Optional filter by star rating
    
    Returns a CSV file with all reviews
    """
    try:
        # Build query
        query = db.query(Review)
        
        # Apply rating filter if provided
        if rating is not None:
            query = query.filter(Review.rating == rating)
        
        # Get all reviews
        reviews = query.order_by(desc(Review.created_at)).all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID',
            'Rating',
            'Review Text',
            'Summary',
            'Recommended Actions',
            'User Response',
            'Created At'
        ])
        
        # Write data
        for review in reviews:
            writer.writerow([
                review.id,
                review.rating,
                review.review_text,
                review.summary or '',
                ', '.join(review.recommended_actions) if review.recommended_actions else '',
                review.user_response or '',
                review.created_at.isoformat()
            ])
        
        # Prepare response
        output.seek(0)
        
        # Generate filename with timestamp
        filename = f"reviews_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error exporting reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to export reviews: {str(e)}")


# Get single review endpoint - MUST come AFTER /priority and /export
@app.get("/api/reviews/{review_id}", response_model=AdminReviewItem)
def get_review(review_id: str, db: Session = Depends(get_db)):
    """
    Get a single review by ID
    
    - **review_id**: UUID of the review
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return AdminReviewItem(
        id=review.id,
        rating=review.rating,
        review_text=review.review_text,
        summary=review.summary,
        recommended_actions=review.recommended_actions,
        user_response=review.user_response,
        created_at=review.created_at
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
