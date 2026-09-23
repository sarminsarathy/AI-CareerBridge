import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'careerbridge.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Student Profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_profiles (
        user_id INTEGER PRIMARY KEY,
        phone TEXT,
        dob TEXT,
        gender TEXT,
        location TEXT,
        education_level TEXT,
        institution TEXT,
        course TEXT,
        graduation_year INTEGER,
        career_interests TEXT, -- JSON array of strings
        profile_completed INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # Master Skills table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills_master (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL
    );
    """)

    # Student Skills table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill_name TEXT NOT NULL,
        category TEXT NOT NULL,
        proficiency TEXT NOT NULL, -- Beginner, Intermediate, Advanced, Expert
        UNIQUE(user_id, skill_name),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # Career Roles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_key TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        avg_salary TEXT NOT NULL
    );
    """)

    # Career Required Skills table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_required_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_id INTEGER NOT NULL,
        skill_name TEXT NOT NULL,
        required_proficiency TEXT NOT NULL, -- Beginner, Intermediate, Advanced, Expert
        importance TEXT NOT NULL, -- High, Medium, Low
        FOREIGN KEY(role_id) REFERENCES career_roles(id) ON DELETE CASCADE
    );
    """)

    # Internships table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS internships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT NOT NULL,
        work_type TEXT NOT NULL, -- Remote, On-site, Hybrid
        duration TEXT NOT NULL,
        stipend TEXT NOT NULL,
        required_skills TEXT NOT NULL, -- JSON array
        description TEXT NOT NULL,
        apply_url TEXT NOT NULL
    );
    """)

    # Jobs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT NOT NULL,
        employment_type TEXT NOT NULL, -- Full-time, Part-time, Contract
        min_experience TEXT NOT NULL,
        required_skills TEXT NOT NULL, -- JSON array
        description TEXT NOT NULL,
        apply_url TEXT NOT NULL
    );
    """)

    # Government Schemes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS government_schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scheme_name TEXT NOT NULL,
        department TEXT NOT NULL,
        target_audience TEXT NOT NULL,
        region TEXT NOT NULL,
        min_education TEXT NOT NULL,
        age_min INTEGER DEFAULT 0,
        age_max INTEGER DEFAULT 100,
        max_family_income INTEGER DEFAULT 0, -- 0 means no cap
        category_criteria TEXT DEFAULT 'All',
        description TEXT NOT NULL,
        official_url TEXT NOT NULL,
        is_demo INTEGER DEFAULT 0
    );
    """)

    # Scheme Documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scheme_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scheme_id INTEGER NOT NULL,
        document_name TEXT NOT NULL,
        reason TEXT NOT NULL,
        FOREIGN KEY(scheme_id) REFERENCES government_schemes(id) ON DELETE CASCADE
    );
    """)

    # Student Document Status table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        document_name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Not Available', -- Available, Not Available, Need to Obtain
        UNIQUE(user_id, document_name),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
