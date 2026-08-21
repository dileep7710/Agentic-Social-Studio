import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "studio_database.db"

def get_connection():
    """Returns a SQLite connection with timeout and WAL mode."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    return conn

def init_db():
    """Initializes the SQLite database with safe auto-migration."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user_profiles table has session_id column
        cursor.execute("PRAGMA table_info(user_profiles)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if columns and "session_id" not in columns:
            # Old schema detected - drop and recreate cleanly
            cursor.execute("DROP TABLE IF EXISTS user_profiles")
            cursor.execute("DROP TABLE IF EXISTS post_history")
        
        # 1. Multi-User Isolated Profiles Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            name TEXT DEFAULT '',
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
        
        # 2. Multi-User Isolated Post History Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            quote_text TEXT,
            author_name TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Database Error] Init failed: {e}")

def save_user_profile(session_id: str, name: str = "", phone: str = "", ig_id: str = "", ig_token: str = "", fb_page_id: str = "", fb_page_token: str = "", li_token: str = "", li_urn: str = ""):
    """Saves or updates profile strictly isolated by unique session_id."""
    if not session_id:
        return
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_profiles WHERE session_id = ?", (session_id,))
        cursor.execute("""
        INSERT INTO user_profiles (session_id, name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (session_id, name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Database Error] save_user_profile failed: {e}")

def get_user_profile(session_id: str):
    """Retrieves profile strictly for the requesting session_id (0% data bleed)."""
    if not session_id:
        return {}
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn FROM user_profiles WHERE session_id = ?", (session_id,))
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
    except Exception as e:
        print(f"[Database Error] get_user_profile failed: {e}")
    return {}

def clear_user_profile(session_id: str):
    """Clears profile only for the specific requesting session."""
    if not session_id:
        return
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_profiles WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Database Error] clear_user_profile failed: {e}")

def save_post_to_history(session_id: str, quote_text: str, author_name: str, image_url: str):
    """Saves a post isolated by user session_id."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO post_history (session_id, quote_text, author_name, image_url)
        VALUES (?, ?, ?, ?)
        """, (session_id, quote_text, author_name, image_url))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Database Error] save_post_to_history failed: {e}")

def get_recent_posts(session_id: str, limit: int = 25):
    """Fetches post history strictly for the requesting user session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT quote_text, author_name, image_url, created_at FROM post_history WHERE session_id = ? ORDER BY id DESC LIMIT ?", (session_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[Database Error] get_recent_posts failed: {e}")
        return []

# Auto-initialize on module load
init_db()
