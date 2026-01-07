# FastAPI Backend Deployment Guide

## Option 1: Deploy to Render (Recommended - Free Tier)

### Prerequisites
- GitHub account
- Render account (sign up at render.com)

### Steps:

1. **Prepare the Backend**
   - Add `requirements.txt` with all dependencies
   - Add `render.yaml` for configuration
   - Push code to GitHub

2. **Deploy on Render**
   - Go to render.com → New → Web Service
   - Connect your GitHub repository
   - Select the `TASK2` folder
   - Render will auto-detect Python and use `requirements.txt`
   - Set environment variables (GEMINI_API_KEY)
   - Click "Create Web Service"

3. **Get Your API URL**
   - Render will give you a URL like: `https://your-app.onrender.com`
   - Use this URL in your frontend `.env` files

---

## Option 2: Deploy to Railway (Alternative - Free Tier)

### Steps:

1. **Sign up at railway.app**
2. **New Project → Deploy from GitHub**
3. **Select your repository**
4. **Add environment variables:**
   - `GEMINI_API_KEY=your_key`
5. **Railway auto-deploys**

---

## Option 3: Deploy to Google Cloud Run (Scalable)

### Steps:

1. **Install Google Cloud CLI**
2. **Build Docker image:**
   ```bash
   docker build -t gcr.io/YOUR_PROJECT/review-api .
   ```
3. **Push to Google Container Registry:**
   ```bash
   docker push gcr.io/YOUR_PROJECT/review-api
   ```
4. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy review-api --image gcr.io/YOUR_PROJECT/review-api --platform managed
   ```

---

## Important: Update CORS Settings

After deployment, update `main.py` CORS to allow your frontend domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-vendor-app.vercel.app",
        "https://your-admin-app.vercel.app",
        "http://localhost:5173",  # Keep for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Database Considerations

**Current:** SQLite (file-based, not suitable for cloud)

**For Production:** Switch to PostgreSQL

### Quick PostgreSQL Setup on Render:
1. Create a PostgreSQL database on Render (free tier)
2. Get connection URL
3. Update `database.py` to use PostgreSQL:
   ```python
   DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./reviews.db")
   ```
4. Add to requirements.txt:
   ```
   psycopg2-binary
   ```

---

## Cost Estimate

| Service | Tier | Cost |
|---------|------|------|
| Vercel (Vendor) | Free | $0 |
| Vercel (Admin) | Free | $0 |
| Render (API) | Free | $0 |
| Render (PostgreSQL) | Free | $0 |
| **Total** | | **$0/month** |

**Note:** Free tiers have limitations (sleep after inactivity, limited resources)

For production with better performance:
- Render Pro: $7/month
- Railway Pro: $5/month
