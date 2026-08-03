from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

import random
from database.database import init_db

init_db()
app = FastAPI(title="Click To Earn API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # পরে চাইলে Netlify URL দিয়ে সীমাবদ্ধ করবে
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
ref_code = "RF" + str(user.user_id)
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
@app.post("/daily/{user_id}")
def daily_bonus(user_id: int):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET balance = balance + 1 WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "reward": 1
    }
@app.post("/reward/{user_id}")
def reward(user_id: int):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET balance = balance + 1 WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return {"success": True}
@app.get("/referral/{user_id}")
def referral(user_id: int):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT ref_code, referrals FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()
    conn.close()

    if row:
        return {
            "ref_code": row[0],
            "referrals": row[1]
        }

    return {
        "ref_code": "",
        "referrals": 0
    }
@app.post("/referral")
def apply_referral(data: dict):

    user_id = data["user_id"]
    ref_code = data["ref_code"]

    conn = get_db()
    cur = conn.cursor()

    # নিজের কোড ব্যবহার করা যাবে না
    cur.execute(
        "SELECT user_id FROM users WHERE ref_code=?",
        (ref_code,)
    )

    owner = cur.fetchone()

    if not owner:
        conn.close()
        return {"success": False}

    owner_id = owner[0]

    if owner_id == user_id:
        conn.close()
        return {"success": False}

    # আগে Referral ব্যবহার করেছে কি না
    cur.execute(
        "SELECT referred_by FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    if row and row[0] != 0:
        conn.close()
        return {"success": False}

    # নতুন User-কে Mark করো
    cur.execute(
        "UPDATE users SET referred_by=? WHERE user_id=?",
        (owner_id, user_id)
    )

    # Referrer Reward
    cur.execute(
        "UPDATE users SET balance=balance+1, referrals=referrals+1 WHERE user_id=?",
        (owner_id,)
    )

    conn.commit()
    conn.close()

    return {"success": True}
from fastapi import Request

@app.get("/postback")
def postback(
    telegram_id: int,
    reward: str = "",
    price: float = 0
):

    if reward != "yes":
        return {"success": False}

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET balance = balance + 1 WHERE user_id=?",
        (telegram_id,)
    )

    conn.commit()
    conn.close()

    return {"success": True}
