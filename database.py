import sqlite3
import tempfile
import os
from pathlib import Path

# Use safe database path with write permissions
DB_PATH = Path(tempfile.gettempdir()) / "agentic_studio_database.db"

# In-memory session store fallback
_IN_MEMORY_PROFILES = {}
_IN_MEMORY_POSTS = {}

def get_connection():
    """Returns a SQLite connection with timeout."""
    try:
        conn = sqlite3.connect(str(DB_PATH), timeout=15.0)
        return conn
    except Exception:
        return None

def init_db():
    """Initializes the SQLite database tables safely."""
    try:
        conn = get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            session_id TEXT PRIMARY KEY,
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
        print(f"[Database Notice] Init fallback to memory: {e}")

def save_user_profile(session_id: str, name: str = "", phone: str = "", ig_id: str = "", ig_token: str = "", fb_page_id: str = "", fb_page_token: str = "", li_token: str = "", li_urn: str = ""):
    """Saves profile to SQLite with memory fallback (Zero Error Guarantee)."""
    if not session_id:
        return
    
    # Save to memory cache
    _IN_MEMORY_PROFILES[session_id] = {
        "name": name,
        "phone": phone,
        "ig_id": ig_id,
        "ig_token": ig_token,
        "fb_page_id": fb_page_id,
        "fb_page_token": fb_page_token,
        "li_token": li_token,
        "li_urn": li_urn
    }
    
    try:
        conn = get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_profiles WHERE session_id = ?", (session_id,))
        cursor.execute("""
        INSERT INTO user_profiles (session_id, name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session_id, name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Database Notice] Saved to memory cache ({e})")

def get_user_profile(session_id: str):
    """Retrieves profile strictly for session_id with memory fallback."""
    if not session_id:
        return {}
    
    # Check memory first
    if session_id in _IN_MEMORY_PROFILES:
        return _IN_MEMORY_PROFILES[session_id]
        
    try:
        conn = get_connection()
        if not conn:
            return {}
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, ig_id, ig_token, fb_page_id, fb_page_token, li_token, li_urn FROM user_profiles WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            data = {
                "name": row[0] or "",
                "phone": row[1] or "",
                "ig_id": row[2] or "",
                "ig_token": row[3] or "",
                "fb_page_id": row[4] or "",
                "fb_page_token": row[5] or "",
                "li_token": row[6] or "",
                "li_urn": row[7] or ""
            }
            _IN_MEMORY_PROFILES[session_id] = data
            return data
    except Exception as e:
        print(f"[Database Notice] Read notice ({e})")
    return {}

def clear_user_profile(session_id: str):
    """Clears profile for session_id."""
    if not session_id:
        return
    _IN_MEMORY_PROFILES.pop(session_id, None)
    try:
        conn = get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_profiles WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        pass

def save_post_to_history(session_id: str, quote_text: str, author_name: str, image_url: str):
    """Saves post history with memory fallback."""
    if session_id not in _IN_MEMORY_POSTS:
        _IN_MEMORY_POSTS[session_id] = []
    _IN_MEMORY_POSTS[session_id].append((quote_text, author_name, image_url, "Just now"))
    
    try:
        conn = get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO post_history (session_id, quote_text, author_name, image_url)
        VALUES (?, ?, ?, ?)
        """, (session_id, quote_text, author_name, image_url))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_recent_posts(session_id: str, limit: int = 25):
    """Fetches post history strictly for session_id."""
    results = []
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT quote_text, author_name, image_url, created_at FROM post_history WHERE session_id = ? ORDER BY id DESC LIMIT ?", (session_id, limit))
            results = cursor.fetchall()
            conn.close()
    except Exception:
        pass
    
    if not results and session_id in _IN_MEMORY_POSTS:
        return list(reversed(_IN_MEMORY_POSTS[session_id]))[:limit]
    return results

# Initialize on module load
init_db()
