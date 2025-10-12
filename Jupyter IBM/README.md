# 🎯 CareerSight AI - Enterprise Edition

> AI-Powered Career Intelligence Platform for Smart Job Matching & Career Development

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🌟 Overview

CareerSight AI is an enterprise-grade career intelligence platform that leverages artificial intelligence 
to provide personalized job recommendations, market insights, and career development guidance.

### Key Technologies
- **Frontend**: Streamlit (Interactive Web UI)
- **Backend**: Python 3.8+, FastAPI
- **AI/ML**: Google Gemini AI, Scikit-learn
- **Database**: SQLite/PostgreSQL
- **Visualization**: Plotly, Matplotlib
- **Authentication**: JWT, bcrypt

## ✨ Features

### 🎯 Core Features
- **AI-Powered Job Matching**: Intelligent recommendation engine
- **Resume Analysis**: Automated resume parsing and scoring
- **Market Insights**: Real-time job market analytics
- **Career Path Planning**: Personalized career roadmaps
- **Skill Gap Analysis**: Identify areas for improvement
- **Email Notifications**: Automated job alerts

### 🔧 Technical Features
- RESTful API endpoints
- User authentication & authorization
- Database migrations & seeding
- Comprehensive logging
- Unit & integration tests
- Code quality checks (Black, Flake8, isort)

## 📁 Project Structure

```
CareerSightAI/
├── app.py                      # Main Streamlit application
├── main.py                     # Alternative entry point
├── init_db.py                  # Database initialization
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project configuration
├── .env.example               # Environment variables template
│
├── src/                       # Source code
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── logger.py          # Logging setup
│   │   └── security.py        # Authentication & security
│   │
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   ├── job.py             # Job model
│   │   └── application.py     # Application model
│   │
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── ai_service.py      # AI/ML services
│   │   ├── job_service.py     # Job-related services
│   │   └── user_service.py    # User management
│   │
│   └── api/                   # API routes
│       ├── __init__.py
│       ├── endpoints/
│       │   ├── jobs.py
│       │   ├── users.py
│       │   └── recommendations.py
│       └── dependencies.py
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── data_processor.py      # Data processing utilities
│   ├── database.py            # Database operations
│   ├── gemini_integration.py  # Google Gemini AI integration
│   ├── market_insights.py     # Market analysis
│   ├── recommendation_engine.py # Recommendation system
│   ├── resume_builder.py      # Resume building
│   ├── email_notifications.py # Email system
│   ├── validators.py          # Input validation
│   ├── helpers.py             # Helper functions
│   └── constants.py           # Application constants
│
├── data/                      # Data files
│   ├── __init__.py
│   ├── sample_jobs.py         # Sample job data
│   ├── skills_taxonomy.json   # Skills database
│   └── industries.json        # Industry classifications
│
├── assets/                    # Static assets
│   ├── images/
│   │   ├── logo.png
│   │   └── favicon.ico
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── analytics.js
│
├── pages/                     # Streamlit pages
│   ├── 1_🏠_Dashboard.py
│   ├── 2_🔍_Job_Search.py
│   ├── 3_📊_Analytics.py
│   ├── 4_📝_Resume_Builder.py
│   └── 5_⚙️_Settings.py
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_database.py
│   │   ├── test_recommender.py
│   │   └── test_ai_service.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_workflows.py
│   └── fixtures/
│       └── sample_data.py
│
├── scripts/                   # Utility scripts
│   ├── setup.sh               # Setup script
│   ├── deploy.sh              # Deployment script
│   ├── seed_data.py           # Database seeding
│   └── backup_db.py           # Database backup
│
├── docs/                      # Documentation
│   ├── API.md                 # API documentation
│   ├── ARCHITECTURE.md        # Architecture guide
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── CONTRIBUTING.md        # Contribution guidelines
│
├── migrations/                # Database migrations
│   ├── versions/
│   │   └── 001_initial.py
│   └── alembic.ini
│
├── logs/                      # Application logs
│   └── .gitkeep
│
└── .streamlit/               # Streamlit configuration
    └── config.toml
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip or poetry
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/careersight-ai.git
cd careersight-ai
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 5: Initialize Database
```bash
python init_db.py
python scripts/seed_data.py
```

### Step 6: Run Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables
See `.env.example` for all available configuration options.

### Key Configurations
- **GEMINI_API_KEY**: Required for AI features
- **DATABASE_URL**: Database connection string
- **EMAIL_***: Email notification settings
- **SECRET_KEY**: For session management

## 📖 Usage

### Web Interface
1. Open browser to `http://localhost:8501`
2. Create account or login
3. Upload resume or enter profile
4. Browse job recommendations
5. Apply to jobs and track applications

### API Access
```bash
# Start API server
uvicorn src.api.main:app --reload

# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest --cov=src tests/
```

### Run Specific Test Suite
```bash
pytest tests/unit/
pytest tests/integration/
```

## 🚢 Deployment

### Docker
```bash
docker build -t careersight-ai .
docker run -p 8501:8501 careersight-ai
```

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository in Streamlit Cloud
3. Configure secrets
4. Deploy

See `docs/DEPLOYMENT.md` for detailed instructions.

## 🤝 Contributing

We welcome contributions! Please see `docs/CONTRIBUTING.md` for guidelines.

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run linters
black src/ tests/
flake8 src/ tests/
isort src/ tests/

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Authors

- **Your Name** - Initial work

## 🙏 Acknowledgments

- Google Gemini AI for AI capabilities
- Streamlit for the amazing framework
- The open-source community

## 📧 Contact

For questions or support, please email: support@careersight.ai

---

Made with ❤️ by the CareerSight AI Team
