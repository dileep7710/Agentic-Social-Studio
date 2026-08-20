import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "studio_database.db"

def init_db():
    """Initializes the SQLite database tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. User Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 2. Post History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS post_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote_text TEXT,
        author_name TEXT,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_user_profile(name: str, phone: str):
    """Saves or updates user profile in database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_profiles")
    cursor.execute("INSERT INTO user_profiles (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

def get_user_profile():
    """Retrieves saved user profile."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM user_profiles ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0], row[1]
    return "", ""

def save_post_to_history(quote_text: str, author_name: str, image_url: str):
    """Saves a generated post into history database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO post_history (quote_text, author_name, image_url)
    VALUES (?, ?, ?)
    """, (quote_text, author_name, image_url))
    conn.commit()
    conn.close()

def get_recent_posts(limit: int = 10):
    """Fetches recent post history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT quote_text, author_name, image_url, created_at FROM post_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Auto-initialize on module load
init_db()
