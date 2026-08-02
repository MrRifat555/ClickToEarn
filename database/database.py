import sqlite3

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        balance REAL DEFAULT 0,
        referrals INTEGER DEFAULT 0
ref_code TEXT UNIQUE,
referred_by INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
