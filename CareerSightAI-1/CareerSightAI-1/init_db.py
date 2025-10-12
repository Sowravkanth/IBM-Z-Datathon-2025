#!/usr/bin/env python3
"""Initialize the database schema"""

from utils.database import Database

if __name__ == "__main__":
    print("Initializing database...")
    db = Database()
    db.init_db()
    print("Database initialized successfully!")
    print("Tables created: users, job_applications, saved_searches, email_preferences")
