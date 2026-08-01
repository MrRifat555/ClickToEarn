from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Click To Earn API")

DB = "users.db"

def get_db():
    return sqlite3.connect(DB)

class User(BaseModel):
    user_id: int
    username: str = ""
    first_name: str = ""

@app.get("/")
def home():
    return {
        "status": "online",
        "project": "Click To Earn API"
    }

@app.post("/login")
def login(user: User):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users
    (user_id, username, first_name, balance, referrals)
    VALUES(?,?,?,?,?)
    """,
    (
        user.user_id,
        user.username,
        user.first_name,
        0,
        0
    ))

    conn.commit()
    conn.close()

    return {
        "success": True
    }

@app.get("/balance/{user_id}")
def balance(user_id: int):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return {
            "balance": row[0]
        }

    return {
        "balance": 0
    }
