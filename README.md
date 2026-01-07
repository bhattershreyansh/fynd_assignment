# Fynd Assignment - Complete Solution

**Author:** Shreyansh Bhatter  
**Date:** January 7, 2026  
**Repository:** https://github.com/bhattershreyansh/fynd_assignment

---

## 📁 Project Structure

```
fynd/
├── TASK1/              # Prompt Engineering Evaluation
│   ├── task1_groq.ipynb
│   ├── PROMPT_EVALUATION_REPORT.md
│   ├── yelp.csv
│   └── results/
├── TASK2/              # FastAPI Backend with AI Integration
│   ├── main.py
│   ├── ai_service.py
│   ├── database.py
│   └── models.py
├── vendor/             # Customer-Facing Review App
│   └── src/
└── admin/              # Admin Dashboard
    └── src/
```

---

## 🎯 Assignment Overview

This repository contains solutions for a full-stack review management system with AI integration:

### **TASK 1: Prompt Engineering** 📝
Evaluation of 3 different prompt strategies for predicting Yelp review star ratings using LLMs.

### **TASK 2: Backend Development** 🔧
FastAPI backend with Google Gemini AI integration for review analysis and insights.

### **Vendor App: Customer Interface** ⭐
React/TypeScript frontend for customers to submit reviews with personalized AI responses.

### **Admin App: Management Dashboard** 📊
React/TypeScript admin panel for review management, analytics, and priority queue.

---

## 📝 TASK 1: Prompt Engineering Evaluation

### Overview
Comprehensive evaluation of prompt engineering strategies for star rating prediction from review text.

### Prompts Evaluated
1. **Basic Prompt** - Simple, direct instruction
2. **Chain-of-Thought** - Guided reasoning steps
3. **Few-Shot Learning** - Learning by example

### Results Summary
| Prompt | Accuracy | JSON Validity | Consistency |
|--------|----------|---------------|-------------|
| **Prompt 1 (Basic)** | 62.00% | **100%** ⭐ | **0.508** ⭐ |
| Prompt 2 (CoT) | 59.00% | **100%** ⭐ | 0.534 |
| Prompt 3 (Few-Shot) | **63.51%** ⭐ | 74.00% | 0.512 |

**Recommendation:** Prompt 1 (Basic) for production use due to perfect reliability.

### Files
- `task1_groq.ipynb` - Complete evaluation notebook
- `PROMPT_EVALUATION_REPORT.md` - Detailed analysis report (PDF-ready)
- `prompt_comparison_results.csv` - Metrics comparison
- `prompt_evaluation_results.png` - Visual comparison charts
- `detailed_predictions.json` - Full prediction data

### Tech Stack
- **Model:** Groq API (llama-3.3-70b-versatile)
- **Dataset:** 100 Yelp reviews
- **Libraries:** pandas, scikit-learn, matplotlib, seaborn

---

## 🔧 TASK 2: Backend API

### Features
- 🤖 **AI-Powered Analysis** - Google Gemini integration
- 📝 **Review Processing** - Automatic summary generation
- 💡 **Smart Recommendations** - AI-generated action items
- 👤 **Personalization** - Name-based personalized responses
- 🗄️ **Database** - SQLAlchemy ORM with SQLite/PostgreSQL
- � **Analytics** - Real-time metrics and insights

### API Endpoints
```
POST   /api/reviews          # Submit new review
GET    /api/reviews          # Get all reviews (paginated)
GET    /api/analytics        # Get dashboard analytics
GET    /api/reviews/priority # Get urgent reviews (1-2 stars)
GET    /api/reviews/export   # Export reviews as CSV
```

### Setup
```bash
cd TASK2
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Add your GEMINI_API_KEY
python main.py
```

**Backend runs on:** `http://localhost:8000`  
**API Docs:** `http://localhost:8000/docs`

---

## ⭐ Vendor App (Customer Interface)

### Features
- ⭐ **Star Rating System** (1-5)
- � **Review Submission** with validation
- 👤 **Name Field** for personalized responses
- 🤖 **AI-Generated Responses** - Personalized thank you messages
- ✅ **Real-Time Feedback** - Instant confirmation

### Setup
```bash
cd vendor
npm install
cp .env.example .env
npm run dev
```

**Runs on:** `http://localhost:5173`

### Tech Stack
- React 18 + TypeScript
- Vite
- TailwindCSS
- Lucide Icons

---

## � Admin App (Management Dashboard)

### Features
- 📊 **Analytics Dashboard** - Key metrics and trends
- 📋 **Review Management** - Pagination & filtering
- 🚨 **Priority Queue** - Urgent reviews (1-2 stars)
- 📥 **CSV Export** - Download review data
- 🔐 **Authentication** - Demo login system

### Setup
```bash
cd admin
npm install
cp .env.example .env
npm run dev
```

**Runs on:** `http://localhost:5174`

### Login Credentials
- **Email:** `admin@example.com`
- **Password:** `admin123`

---

## 🚀 Quick Start (All Services)

### 1. Clone Repository
```bash
git clone https://github.com/bhattershreyansh/fynd_assignment.git
cd fynd
```

### 2. Setup Environment Variables
```bash
# Backend
cd TASK2
cp .env.example .env
# Add your GEMINI_API_KEY

# Vendor
cd ../vendor
cp .env.example .env

# Admin
cd ../admin
cp .env.example .env
```

### 3. Start Backend
```bash
cd TASK2
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 4. Start Vendor App (New Terminal)
```bash
cd vendor
npm install
npm run dev
```

### 5. Start Admin App (New Terminal)
```bash
cd admin
npm install
npm run dev
```

### 6. Access Applications
- **Vendor:** http://localhost:5173
- **Admin:** http://localhost:5174
- **API Docs:** http://localhost:8000/docs

---

## �️ Tech Stack Summary

| Component | Technologies |
|-----------|-------------|
| **TASK 1** | Python, Groq API, Jupyter, pandas, scikit-learn |
| **Backend** | FastAPI, SQLAlchemy, Google Gemini AI, Python 3.10+ |
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **Deployment** | Render (backend), Vercel (frontend) |

---

## 📦 Deployment

### Backend (Render)
See [`TASK2/DEPLOYMENT.md`](TASK2/DEPLOYMENT.md)
- Free tier available
- PostgreSQL database recommended

### Vendor Frontend (Vercel)
See [`vendor/DEPLOYMENT.md`](vendor/DEPLOYMENT.md)
- Free tier available
- Automatic deployments from GitHub

### Admin Frontend (Vercel)
See [`admin/DEPLOYMENT.md`](admin/DEPLOYMENT.md)
- Free tier available
- Automatic deployments from GitHub

---

## � Key Features Implemented

### ✅ TASK 1 Requirements
- [x] 3 different prompt strategies
- [x] Clear explanation of each prompt
- [x] Evaluation on 100 reviews
- [x] Comparison table with metrics
- [x] Discussion of results and trade-offs
- [x] Comprehensive report (PDF-ready)

### ✅ TASK 2 Requirements
- [x] FastAPI backend
- [x] Google Gemini AI integration
- [x] Review submission endpoint
- [x] AI-powered summary generation
- [x] Recommended actions for admins
- [x] Personalized user responses
- [x] Database integration (SQLAlchemy)

### ✅ Additional Features
- [x] Vendor app with personalized responses
- [x] Admin dashboard with analytics
- [x] Priority queue for urgent reviews
- [x] CSV export functionality
- [x] Complete deployment guides
- [x] Comprehensive documentation

---

## 🔒 Security Notes

- All `.env` files are gitignored
- Never commit API keys or secrets
- Admin uses demo authentication (replace for production)
- Update CORS settings for production domains
- Database file (`reviews.db`) is gitignored

---

## � Project Highlights

### Innovation
- **Personalized AI Responses** - Name-based personalization in vendor app
- **Priority Queue** - Smart filtering of urgent reviews
- **Real-Time Analytics** - Live dashboard metrics

### Code Quality
- **TypeScript** - Type-safe frontend code
- **Pydantic Models** - Validated API requests/responses
- **Modular Architecture** - Separation of concerns

### Documentation
- Comprehensive README files
- API documentation (Swagger/ReDoc)
- Deployment guides for all services
- Detailed prompt evaluation report

---

## �📄 Documentation

- **Main README:** This file
- **TASK 1 Report:** [`TASK1/PROMPT_EVALUATION_REPORT.md`](TASK1/PROMPT_EVALUATION_REPORT.md)
- **Backend README:** [`TASK2/README.md`](TASK2/README.md)
- **Backend Deployment:** [`TASK2/DEPLOYMENT.md`](TASK2/DEPLOYMENT.md)
- **Vendor Deployment:** [`vendor/DEPLOYMENT.md`](vendor/DEPLOYMENT.md)
- **Admin Deployment:** [`admin/DEPLOYMENT.md`](admin/DEPLOYMENT.md)

---

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- **Prompt Engineering** - Systematic evaluation of LLM prompts
- **Full-Stack Development** - React + FastAPI integration
- **AI Integration** - Google Gemini API usage
- **Database Design** - SQLAlchemy ORM patterns
- **API Development** - RESTful API design
- **Frontend Development** - React + TypeScript best practices
- **Deployment** - Cloud deployment strategies

---

## 📧 Contact

**Shreyansh Bhatter**  
GitHub: [@bhattershreyansh](https://github.com/bhattershreyansh)

---

## 📄 License

This project is for educational/demonstration purposes.

---

## 🙏 Acknowledgments

- **Groq** - Fast LLM inference for prompt evaluation
- **Google Gemini** - AI-powered review analysis
- **FastAPI** - Modern Python web framework
- **React** - Frontend framework
- **Vercel & Render** - Deployment platforms
