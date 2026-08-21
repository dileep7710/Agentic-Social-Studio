import os
import sqlite3
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, SocialAccount
from backend.crypto import encrypt_token

DB_PATH = Path(__file__).parent / "agent_studio.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH.resolve()}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_migrations():
    """Performs safe, non-destructive column and table migrations on existing SQLite database."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Check users table columns
        cursor.execute("PRAGMA table_info(users)")
        user_cols = [row[1] for row in cursor.fetchall()]
        if user_cols:
            if "failed_login_attempts" not in user_cols:
                cursor.execute("ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0")
            if "locked_until" not in user_cols:
                cursor.execute("ALTER TABLE users ADD COLUMN locked_until TIMESTAMP")
            if "last_login_at" not in user_cols:
                cursor.execute("ALTER TABLE users ADD COLUMN last_login_at TIMESTAMP")
            if "password_changed_at" not in user_cols:
                cursor.execute("ALTER TABLE users ADD COLUMN password_changed_at TIMESTAMP")

        # Check social_accounts table columns
        cursor.execute("PRAGMA table_info(social_accounts)")
        social_cols = [row[1] for row in cursor.fetchall()]
        if social_cols:
            if "scopes" not in social_cols:
                cursor.execute("ALTER TABLE social_accounts ADD COLUMN scopes VARCHAR(255) DEFAULT ''")
            if "token_type" not in social_cols:
                cursor.execute("ALTER TABLE social_accounts ADD COLUMN token_type VARCHAR(50) DEFAULT 'Bearer'")

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Database Migration Notice] Safe migration notice: {e}")

    # Auto-encrypt any legacy unencrypted tokens at rest
    try:
        db = SessionLocal()
        accounts = db.query(SocialAccount).all()
        migrated = 0
        for acc in accounts:
            changed = False
            if acc.access_token and not acc.access_token.startswith("aes_gcm:v1:"):
                acc.access_token = encrypt_token(acc.access_token)
                changed = True
            if acc.refresh_token and not acc.refresh_token.startswith("aes_gcm:v1:"):
                acc.refresh_token = encrypt_token(acc.refresh_token)
                changed = True
            if changed:
                migrated += 1
        if migrated > 0:
            db.commit()
            print(f"[Database Migration] Successfully encrypted {migrated} legacy OAuth token records with AES-256-GCM.")
        db.close()
    except Exception as e:
        print(f"[Database Migration Notice] Token encryption migration notice: {e}")


def init_db():
    Base.metadata.create_all(bind=engine)
    run_migrations()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Auto-initialize and migrate tables
init_db()
