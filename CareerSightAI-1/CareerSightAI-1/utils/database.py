import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import json
from typing import Optional, Dict, List, Any

class Database:
    """Database utility for CareerSight AI"""
    
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        if not self.database_url:
            self.database_url = None
            self.initialized = False
        else:
            self.initialized = True
            # Auto-initialize tables on first connection
            try:
                self.init_db()
            except Exception as e:
                print(f"Warning: Could not initialize database: {e}")
    
    @contextmanager
    def get_connection(self):
        """Get a database connection context manager"""
        if not self.initialized or not self.database_url:
            raise ValueError("Database not initialized")
        conn = psycopg2.connect(self.database_url)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def is_available(self) -> bool:
        """Check if database is available"""
        return self.initialized and self.database_url is not None
    
    def init_db(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table for profile storage
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100) UNIQUE NOT NULL,
                    skills TEXT,
                    experience_level VARCHAR(50),
                    interests TEXT,
                    location VARCHAR(100),
                    salary_min INTEGER,
                    salary_max INTEGER,
                    industry VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Job applications table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_applications (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100) NOT NULL,
                    job_title VARCHAR(200) NOT NULL,
                    company VARCHAR(200) NOT NULL,
                    location VARCHAR(100),
                    salary_min FLOAT,
                    salary_max FLOAT,
                    skills TEXT,
                    status VARCHAR(50) DEFAULT 'Applied',
                    notes TEXT,
                    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            
            # Saved searches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_searches (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100) NOT NULL,
                    search_name VARCHAR(200) NOT NULL,
                    filters JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            
            # Email preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_preferences (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(200),
                    job_alerts BOOLEAN DEFAULT TRUE,
                    roadmap_reminders BOOLEAN DEFAULT TRUE,
                    weekly_digest BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            
            cursor.close()
    
    def save_user_profile(self, user_id: str, profile: Dict[str, Any]) -> bool:
        """Save or update user profile"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (user_id, skills, experience_level, interests, location, salary_min, salary_max, industry, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    skills = EXCLUDED.skills,
                    experience_level = EXCLUDED.experience_level,
                    interests = EXCLUDED.interests,
                    location = EXCLUDED.location,
                    salary_min = EXCLUDED.salary_min,
                    salary_max = EXCLUDED.salary_max,
                    industry = EXCLUDED.industry,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                user_id,
                profile.get('skills', ''),
                profile.get('experience_level', ''),
                profile.get('interests', ''),
                profile.get('location', ''),
                profile.get('salary_min', 0),
                profile.get('salary_max', 0),
                profile.get('industry', '')
            ))
            
            cursor.close()
            return True
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by user_id"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT user_id, skills, experience_level, interests, location, 
                       salary_min, salary_max, industry, created_at, updated_at
                FROM users 
                WHERE user_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            
            return dict(result) if result else None
    
    def save_job_application(self, user_id: str, job_data: Dict[str, Any]) -> int:
        """Save a job application"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO job_applications 
                (user_id, job_title, company, location, salary_min, salary_max, skills, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                user_id,
                job_data.get('job_title', ''),
                job_data.get('company', ''),
                job_data.get('location', ''),
                job_data.get('salary_min'),
                job_data.get('salary_max'),
                job_data.get('skills', ''),
                job_data.get('status', 'Applied'),
                job_data.get('notes', '')
            ))
            
            app_id = cursor.fetchone()[0]
            cursor.close()
            return app_id
    
    def get_user_applications(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all job applications for a user"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT id, job_title, company, location, salary_min, salary_max, 
                       skills, status, notes, applied_date
                FROM job_applications 
                WHERE user_id = %s
                ORDER BY applied_date DESC
            """, (user_id,))
            
            results = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in results]
    
    def update_application_status(self, app_id: int, status: str, notes: str = None) -> bool:
        """Update job application status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if notes:
                cursor.execute("""
                    UPDATE job_applications 
                    SET status = %s, notes = %s
                    WHERE id = %s
                """, (status, notes, app_id))
            else:
                cursor.execute("""
                    UPDATE job_applications 
                    SET status = %s
                    WHERE id = %s
                """, (status, app_id))
            
            cursor.close()
            return True
    
    def save_search(self, user_id: str, search_name: str, filters: Dict[str, Any]) -> int:
        """Save a search with filters"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO saved_searches (user_id, search_name, filters)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (user_id, search_name, json.dumps(filters)))
            
            search_id = cursor.fetchone()[0]
            cursor.close()
            return search_id
    
    def get_user_searches(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all saved searches for a user"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT id, search_name, filters, created_at
                FROM saved_searches 
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))
            
            results = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in results]
    
    def delete_search(self, search_id: int) -> bool:
        """Delete a saved search"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM saved_searches WHERE id = %s
            """, (search_id,))
            
            cursor.close()
            return True
    
    def save_email_preferences(self, user_id: str, email: str, preferences: Dict[str, bool]) -> bool:
        """Save email notification preferences"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO email_preferences 
                (user_id, email, job_alerts, roadmap_reminders, weekly_digest)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id)
                DO UPDATE SET
                    email = EXCLUDED.email,
                    job_alerts = EXCLUDED.job_alerts,
                    roadmap_reminders = EXCLUDED.roadmap_reminders,
                    weekly_digest = EXCLUDED.weekly_digest
            """, (
                user_id,
                email,
                preferences.get('job_alerts', True),
                preferences.get('roadmap_reminders', True),
                preferences.get('weekly_digest', True)
            ))
            
            cursor.close()
            return True
    
    def get_email_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get email notification preferences"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT email, job_alerts, roadmap_reminders, weekly_digest
                FROM email_preferences 
                WHERE user_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            
            return dict(result) if result else None
