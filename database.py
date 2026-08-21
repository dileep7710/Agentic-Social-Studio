import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "studio_database.db"

def init_db():
    """Initializes the SQLite database tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. User Profiles & Settings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT DEFAULT 'Dileep Yadav',
        phone TEXT DEFAULT '',
        ig_id TEXT DEFAULT '',
        ig_token TEXT DEFAULT '',
        fb_page_id TEXT DEFAULT '',
        fb_page_token TEXT DEFAULT '',
        li_token TEXT DEFAULT '',
        li_urn TEXT DEFAULT '',
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

def save_user_profile(name: str = "", phone: str = "", ig_id: str = "", ig_token: str = "", fb_page_id: str = "", fb_page_token: str = "", li_token: str = "", li_urn: str = ""):
    """Saves or updates user profile and API tokens in SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_profiles")
    cursor.execute("""
    INSERT INTO user_profiles (name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn))
    conn.commit()
    conn.close()

def get_user_profile():
    """Retrieves saved user profile and tokens from SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn FROM user_profiles ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "name": row[0] or "",
            "phone": row[1] or "",
            "ig_id": row[2] or "",
            "ig_token": row[3] or "",
            "fb_page_id": row[4] or "",
            "fb_page_token": row[5] or "",
            "li_token": row[6] or "",
            "li_urn": row[7] or ""
        }
    return {
        "name": "Dileep Yadav",
        "phone": "+917710278967",
        "ig_id": "17841448994358440",
        "ig_token": "",
        "fb_page_id": "61583785015768",
        "fb_page_token": "",
        "li_token": "",
        "li_urn": "urn:li:person:neomMhUioZ"
    }

def clear_user_profile():
    """Clears user profile from SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_profiles")
    conn.commit()
    conn.close()

def save_post_to_history(quote_text: str, author_name: str, image_url: str):
    """Saves a generated post into persistent history database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO post_history (quote_text, author_name, image_url)
    VALUES (?, ?, ?)
    """, (quote_text, author_name, image_url))
    conn.commit()
    conn.close()

def get_recent_posts(limit: int = 20):
    """Fetches persistent post history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT quote_text, author_name, image_url, created_at FROM post_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Auto-initialize on module load
init_db()
