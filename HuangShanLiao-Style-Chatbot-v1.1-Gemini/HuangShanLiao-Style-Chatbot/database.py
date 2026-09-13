import sqlite3
from datetime import datetime
from pathlib import Path
from config import DB_PATH

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            assistant_message TEXT NOT NULL,
            rating INTEGER,
            correction TEXT,
            created_at TEXT NOT NULL
        )
        """)
        conn.commit()

def save_message(session_id, role, content):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO messages(session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (session_id, role, content, datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit()

def get_history(session_id, limit=12):
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT role, content FROM messages
               WHERE session_id=?
               ORDER BY id DESC LIMIT ?""",
            (session_id, limit)
        ).fetchall()
    return [dict(r) for r in reversed(rows)]

def save_feedback(session_id, user_message, assistant_message, rating, correction=""):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO feedback
               (session_id,user_message,assistant_message,rating,correction,created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                session_id, user_message, assistant_message,
                rating, correction, datetime.now().isoformat(timespec="seconds")
            )
        )
        conn.commit()
