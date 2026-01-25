# AI-Powered Review Management System

**Author:** Shreyansh Bhatter  
**Live Demo:** [https://fynd-assignment-sigma.vercel.app](https://fynd-assignment-sigma.vercel.app)  
**Repository:** [https://github.com/bhattershreyansh/fynd_assignment](https://github.com/bhattershreyansh/fynd_assignment)

---

## 📋 Overview

A full-stack review management platform that leverages AI to analyze customer feedback, generate insights, and provide personalized responses. The system combines prompt engineering research with production-ready applications to deliver comprehensive review analytics and management capabilities.

---

## 📁 Project Architecture

```
fynd/
├── TASK1/              # Prompt Engineering Research
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

## 🎯 Key Components

### **1. Prompt Engineering Research** 📝
Systematic evaluation of 3 prompt strategies for LLM-based star rating prediction from review text.

### **2. Backend API** 🔧
FastAPI backend with Google Gemini AI integration for real-time review analysis and insights.

### **3. Customer Interface** ⭐
React/TypeScript application enabling customers to submit reviews and receive AI-generated personalized responses.

### **4. Admin Dashboard** 📊
Management panel with analytics, review monitoring, priority queue, and data export capabilities.

---

## 📝 Prompt Engineering Research

### Research Overview
Comprehensive evaluation of prompt engineering strategies for star rating prediction using LLMs.

### Methodologies Tested
1. **Basic Prompt** - Direct instruction approach
2. **Chain-of-Thought** - Step-by-step reasoning guidance
3. **Few-Shot Learning** - Example-based learning

### Results

| Prompt Strategy | Accuracy | JSON Validity | Consistency |
|----------------|----------|---------------|-------------|
| **Basic Prompt** | 62.00% | **100%** ⭐ | **0.508** ⭐ |
| Chain-of-Thought | 59.00% | **100%** ⭐ | 0.534 |
| Few-Shot Learning | **63.51%** ⭐ | 74.00% | 0.512 |

**Production Recommendation:** Basic Prompt strategy due to perfect reliability and strong performance.

### Research Deliverables
- `task1_groq.ipynb` - Complete evaluation notebook
- `PROMPT_EVALUATION_REPORT.md` - Detailed analysis and findings
- `prompt_comparison_results.csv` - Quantitative metrics
- `prompt_evaluation_results.png` - Visual comparisons
- `detailed_predictions.json` - Full prediction dataset

### Technology Stack
- **Model:** Groq API (llama-3.3-70b-versatile)
- **Dataset:** 100 Yelp reviews
- **Analysis:** pandas, scikit-learn, matplotlib, seaborn

---

## 🔧 Backend API

### Core Features
- 🤖 **AI-Powered Analysis** - Google Gemini integration for intelligent insights
- 📝 **Review Processing** - Automated summary generation and categorization
- 💡 **Smart Recommendations** - AI-generated actionable insights for businesses
- 👤 **Personalization** - Context-aware, personalized customer responses
- 🗄️ **Database** - SQLAlchemy ORM with SQLite/PostgreSQL support
- 📊 **Analytics** - Real-time metrics and dashboard data

### API Endpoints
```
POST   /api/reviews          # Submit new review
GET    /api/reviews          # Retrieve reviews (paginated)
GET    /api/analytics        # Dashboard analytics
GET    /api/reviews/priority # Urgent reviews (1-2 stars)
GET    /api/reviews/export   # CSV export
```

### Setup Instructions
```bash
cd TASK2
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Add your GEMINI_API_KEY
python main.py
```

**Backend:** `http://localhost:8000`  
**API Documentation:** `http://localhost:8000/docs`

---

## ⭐ Customer Interface

### Features
- ⭐ **Star Rating System** - 1-5 star ratings with visual feedback
- ✍️ **Review Submission** - Form validation and error handling
- 👤 **Name Capture** - Enables personalized AI responses
- 🤖 **AI Responses** - Context-aware thank you messages
- ✅ **Real-Time Feedback** - Instant submission confirmation

### Setup
```bash
cd vendor
npm install
cp .env.example .env
npm run dev
```

**Application:** `http://localhost:5173`

### Tech Stack
- React 18 + TypeScript
- Vite
- TailwindCSS
- Lucide Icons

---

## 📊 Admin Dashboard

### Features
- 📈 **Analytics Dashboard** - Key metrics, trends, and visualizations
- 📋 **Review Management** - Pagination, filtering, and search
- 🚨 **Priority Queue** - Automated filtering of urgent reviews (1-2 stars)
- 📥 **CSV Export** - Download review data for analysis
- 🔐 **Authentication** - Secure login system

### Setup
```bash
cd admin
npm install
cp .env.example .env
npm run dev
```

**Application:** `http://localhost:5174`

### Demo Credentials
- **Email:** `admin@example.com`
- **Password:** `admin123`

---

## 🚀 Quick Start Guide

### 1. Clone Repository
```bash
git clone https://github.com/bhattershreyansh/fynd_assignment.git
cd fynd_assignment
```

### 2. Environment Configuration
```bash
# Backend
cd TASK2
cp .env.example .env
# Add your GEMINI_API_KEY

# Vendor App
cd ../vendor
cp .env.example .env

# Admin Dashboard
cd ../admin
cp .env.example .env
```

### 3. Launch Backend
```bash
cd TASK2
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 4. Launch Customer Interface (New Terminal)
```bash
cd vendor
npm install
npm run dev
```

### 5. Launch Admin Dashboard (New Terminal)
```bash
cd admin
npm install
npm run dev
```

### 6. Access Applications
- **Customer Interface:** http://localhost:5173
- **Admin Dashboard:** http://localhost:5174
- **API Documentation:** http://localhost:8000/docs

---

## 🛠️ Technology Stack

| Component | Technologies |
|-----------|-------------|
| **Research** | Python, Groq API, Jupyter, pandas, scikit-learn |
| **Backend** | FastAPI, SQLAlchemy, Google Gemini AI, Python 3.10+ |
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS |
| **Database** | SQLite (development), PostgreSQL (production) |
| **Deployment** | Render (backend), Vercel (frontend) |

---

## 📦 Deployment

### Backend (Render)
See [`TASK2/DEPLOYMENT.md`](TASK2/DEPLOYMENT.md) for complete instructions.
- Free tier available
- PostgreSQL database recommended for production

### Frontend Applications (Vercel)
- **Customer Interface:** [`vendor/DEPLOYMENT.md`](vendor/DEPLOYMENT.md)
- **Admin Dashboard:** [`admin/DEPLOYMENT.md`](admin/DEPLOYMENT.md)
- Free tier available with automatic GitHub deployments

---

## ✨ Key Features

### AI & Automation
- Personalized AI-generated responses using customer names
- Automated review summarization and sentiment analysis
- Intelligent prioritization of urgent reviews
- Real-time analytics and insights generation

### User Experience
- TypeScript for type-safe, maintainable code
- Responsive design with TailwindCSS
- Real-time feedback and validation
- Intuitive admin dashboard with data visualization

### Architecture & Code Quality
- Pydantic models for validated API contracts
- Modular architecture with clear separation of concerns
- RESTful API design principles
- Comprehensive error handling and logging

---

## 🔒 Security & Best Practices

- Environment variables for sensitive data (`.env` files gitignored)
- API key protection and secure configuration
- Authentication system for admin access
- CORS configuration for production deployments
- Database credentials management

---

## 📚 Documentation

- **Main README:** This file
- **Research Report:** [`TASK1/PROMPT_EVALUATION_REPORT.md`](TASK1/PROMPT_EVALUATION_REPORT.md)
- **Backend Guide:** [`TASK2/README.md`](TASK2/README.md)
- **Deployment Guides:** 
  - [`TASK2/DEPLOYMENT.md`](TASK2/DEPLOYMENT.md)
  - [`vendor/DEPLOYMENT.md`](vendor/DEPLOYMENT.md)
  - [`admin/DEPLOYMENT.md`](admin/DEPLOYMENT.md)

---

## 🎯 Technical Skills Demonstrated

- **AI/ML Integration** - Prompt engineering, LLM API integration, AI-powered features
- **Full-Stack Development** - React + FastAPI architecture
- **Database Design** - SQLAlchemy ORM, schema design, migrations
- **API Development** - RESTful principles, OpenAPI documentation
- **Frontend Engineering** - React + TypeScript, component architecture
- **DevOps** - Cloud deployment, environment management, CI/CD readiness

---

## 📧 Contact

**Shreyansh Bhatter**  
GitHub: [@bhattershreyansh](https://github.com/bhattershreyansh)

---

## 🙏 Acknowledgments

- **Groq** - Fast LLM inference for prompt evaluation research
- **Google Gemini** - AI-powered review analysis capabilities
- **FastAPI** - Modern Python web framework
- **React** - Frontend framework and ecosystem
- **Vercel & Render** - Cloud deployment platforms

---

## 📄 License

MIT License - See LICENSE file for details
