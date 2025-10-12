# CareerSight AI

## Overview

CareerSight AI is an AI-powered career intelligence platform that provides personalized job recommendations, learning roadmaps, and market insights. Built with Streamlit for rapid development, the platform processes job posting data, matches users with suitable opportunities using semantic analysis, identifies skill gaps, and generates customized career development plans. The system emphasizes fast response times (sub-500ms) through cache optimization and provides an accessible, mobile-responsive user experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application with wide layout and expandable sidebar
- **State Management**: Session-based state management storing user profiles, job data, recommendations, and applications
- **Data Caching**: Implements `@st.cache_data` decorator for performance optimization on data loading operations
- **Visualization**: Plotly (Express and Graph Objects) for interactive charts and market insights dashboards
- **Responsive Design**: Mobile-responsive interface with accessibility considerations

**Rationale**: Streamlit was chosen for rapid prototyping and deployment, allowing quick iteration on UI/UX while maintaining a professional appearance. The caching strategy ensures fast load times even with large datasets.

### Backend Architecture

#### Data Processing Pipeline
- **DataProcessor Class**: Normalizes job posting data including titles, salaries, experience levels, skills, and locations
- **Data Cleaning**: Regex-based text standardization and field normalization
- **Pandas-based Processing**: DataFrame operations for efficient bulk data transformations

**Rationale**: Centralized data processing ensures consistent data quality across the platform and enables reliable matching algorithms.

#### Recommendation Engine
- **Algorithm**: TF-IDF vectorization with cosine similarity for semantic job matching
- **Feature Engineering**: Combines job titles, skills, and company information with weighted importance
- **Scikit-learn Integration**: Uses `TfidfVectorizer` with configurable parameters (max_features=5000, bigrams, stop words)
- **Scoring System**: Generates compatibility scores between user profiles and job postings

**Rationale**: TF-IDF with cosine similarity provides interpretable, fast matching results without requiring complex neural networks. This approach balances accuracy with computational efficiency.

#### AI-Powered Features (Gemini Integration)
- **Google Gemini API**: Generates personalized 3-month learning roadmaps
- **Structured Prompting**: Template-based prompts for consistent roadmap generation
- **Skills Gap Analysis**: Compares user skills against job requirements to identify development areas
- **Conversational Guidance**: Provides career coaching through natural language interface

**Rationale**: Gemini API enables advanced natural language generation for personalized content without building custom ML models, accelerating development while maintaining quality.

#### Market Intelligence
- **Analytics Engine**: Aggregates job posting data to identify trends
- **Insight Generation**: Tracks top companies, locations, skills demand, salary benchmarks, and role trends
- **Statistical Analysis**: Uses NumPy and Pandas for salary insights, experience distributions, and correlations
- **Visualization Pipeline**: Prepares structured data for Plotly chart generation

**Rationale**: Real-time market insights help users make informed career decisions based on current market conditions rather than outdated information.

### Data Storage Architecture

#### Database Design
- **Primary Database**: PostgreSQL with psycopg2 driver
- **Connection Management**: Context manager pattern for safe connection handling with automatic rollback
- **Schema**:
  - `users` table: User profiles and credentials
  - `job_applications` table: Application tracking
  - `saved_searches` table: User search preferences
  - `email_preferences` table: Notification settings
- **Data Format**: JSON fields for flexible skill and preference storage
- **Initialization**: Auto-initialization on first connection with fallback handling

**Rationale**: PostgreSQL provides robust relational data management with JSON support for semi-structured data. The context manager pattern ensures connection safety and prevents resource leaks.

#### Sample Data System
- **Synthetic Data Generation**: Python-based sample job generator with realistic Indian job market data
- **Data Diversity**: Covers multiple industries, locations, salary ranges, and skill requirements
- **Development Support**: Enables platform testing without external data sources

**Rationale**: Sample data system allows development and testing without dependency on external APIs or real job postings.

### External Dependencies

#### AI/ML Services
- **Google Gemini API**: Natural language generation for learning roadmaps and career guidance
  - API Key: Environment variable `GEMINI_API_KEY`
  - SDK: `google-genai` package
  - Use Case: Personalized roadmap generation, career coaching responses

#### Data Science Stack
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations and array operations
- **Scikit-learn**: Machine learning utilities (TfidfVectorizer, cosine_similarity)

#### Visualization
- **Plotly**: Interactive charts and dashboards
  - Express: High-level chart creation
  - Graph Objects: Custom visualizations

#### Web Framework
- **Streamlit**: Primary web application framework
  - Real-time updates
  - Session state management
  - Component caching

#### Database
- **PostgreSQL**: Primary data storage (optional)
  - Connection: Environment variable `DATABASE_URL`
  - Driver: psycopg2 with RealDictCursor
  - Graceful degradation if unavailable

#### Document Generation
- **ReportLab**: PDF resume generation
  - Professional formatting
  - Custom styling capabilities

#### Email Services (Framework Ready)
- **SMTP Integration**: Email notification system (configurable)
  - Server: Environment variable `SMTP_SERVER` (default: smtp.gmail.com)
  - Port: Environment variable `SMTP_PORT` (default: 587)
  - Credentials: `SENDER_EMAIL`, `SENDER_PASSWORD`
  - Use Cases: Job alerts, roadmap reminders

#### Environment Configuration
All sensitive credentials and service endpoints are managed through environment variables:
- `GEMINI_API_KEY`: Google Gemini authentication
- `DATABASE_URL`: PostgreSQL connection string
- `SMTP_SERVER`, `SMTP_PORT`, `SENDER_EMAIL`, `SENDER_PASSWORD`: Email service configuration

**Design Philosophy**: The architecture prioritizes modularity, with clear separation between data processing, recommendation logic, AI integration, and persistence layers. Each component can operate independently, allowing for easy testing, maintenance, and future enhancements.