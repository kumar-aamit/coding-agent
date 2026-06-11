import sqlite3
from pathlib import Path
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "sqlite:///downtime.db")

def get_connection():
    db_file = Path(DB_PATH).replace("sqlite:///", "")
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS downtime_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME,
            reason TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_downtime(machine_id: str, start_time: str, end_time: str = None, reason: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO downtime_log (machine_id, start_time, end_time, reason)
        VALUES (?, ?, ?, ?)
    """, (machine_id, start_time, end_time, reason))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_downtime_history(machine_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, machine_id, start_time, end_time, reason, created_at
        FROM downtime_log
        WHERE machine_id = ?
        ORDER BY start_time DESC
    """, (machine_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "machine_id": row["machine_id"],
            "start_time": row["start_time"],
            "end_time": row["end_time"],
            "reason": row["reason"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]