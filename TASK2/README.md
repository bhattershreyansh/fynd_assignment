# Review System Backend

FastAPI backend for a review submission system with AI-powered analysis.

## Features

- ✅ User review submission with AI-generated responses
- ✅ Admin dashboard with all reviews and AI insights
- ✅ Server-side LLM processing (Gemini 2.5 Flash)
- ✅ Analytics endpoint
- ✅ Proper error handling and validation
- ✅ CORS enabled for frontend integration

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create a `.env` file in the TASK2 directory:
```
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./reviews.db
```

3. **Run the server:**
```bash
uvicorn main:app --reload
```

Server will start at `http://localhost:8000`

## API Endpoints

### User Endpoints

#### POST `/api/reviews`
Submit a new review
```json
{
  "rating": 4,
  "review_text": "Great service but could be faster"
}
```

Response:
```json
{
  "id": "uuid",
  "rating": 4,
  "review_text": "Great service but could be faster",
  "user_response": "Thank you for your feedback! We're glad...",
  "created_at": "2026-01-07T01:15:00Z",
  "status": "success"
}
```

### Admin Endpoints

#### GET `/api/reviews`
Get all reviews with pagination and filtering
- Query params: `?rating=4&page=1&page_size=50`

#### GET `/api/reviews/{id}`
Get single review by ID

#### GET `/api/analytics`
Get analytics and statistics

#### GET `/api/reviews/priority`
Get urgent reviews (1-2 star ratings) that need immediate attention
- Query params: `?limit=20`
- Returns: List of urgent reviews sorted by most recent

#### GET `/api/reviews/export`
Export reviews to CSV file
- Query params: `?rating=1` (optional filter)
- Returns: CSV file download

## Project Structure

```
TASK2/
├── main.py              # FastAPI application
├── models.py            # Pydantic models
├── database.py          # Database setup
├── ai_service.py        # LLM integration
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
└── reviews.db          # SQLite database (auto-created)
```

## Testing

### Interactive API Docs
Visit `http://localhost:8000/docs` for Swagger UI

### cURL Examples

**Submit a review:**
```bash
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "review_text": "Excellent service! Very professional and quick."}'
```

**Get all reviews:**
```bash
curl http://localhost:8000/api/reviews
```

**Get analytics:**
```bash
curl http://localhost:8000/api/analytics
```

**Get priority reviews:**
```bash
curl http://localhost:8000/api/reviews/priority?limit=10
```

**Export reviews to CSV:**
```bash
curl http://localhost:8000/api/reviews/export -o reviews.csv
```

## Deployment

### Render.com
1. Create new Web Service
2. Connect your repository
3. Set environment variables
4. Deploy!

### Environment Variables for Production
- `GEMINI_API_KEY`: Your Gemini API key
- `DATABASE_URL`: PostgreSQL connection string (for production)

## Error Handling

- Empty reviews: Minimum 10 characters required
- Long reviews: Maximum 5000 characters
- LLM failures: Automatic retry (2 attempts) with fallback responses
- All errors return proper HTTP status codes and error messages
