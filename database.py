import sqlite3
from datetime import date

DB_PATH = "wardrobe.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            category TEXT NOT NULL,
            color TEXT NOT NULL,
            uploaded_at TEXT DEFAULT (date('now'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS usage_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL DEFAULT 'default_user',
            date TEXT NOT NULL,
            outfits_generated INTEGER DEFAULT 0,
            clothes_uploaded INTEGER DEFAULT 0,
            UNIQUE(user_id, date)
        )
    """)

    conn.commit()
    conn.close()

def get_usage(user_id="default_user"):
    conn = get_connection()
    c = conn.cursor()
    today = str(date.today())
    c.execute("SELECT * FROM usage_limits WHERE user_id=? AND date=?", (user_id, today))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"user_id": user_id, "date": today, "outfits_generated": 0, "clothes_uploaded": 0}

def increment_usage(field: str, user_id="default_user"):
    conn = get_connection()
    c = conn.cursor()
    today = str(date.today())
    c.execute("""
        INSERT INTO usage_limits (user_id, date, outfits_generated, clothes_uploaded)
        VALUES (?, ?, 0, 0)
        ON CONFLICT(user_id, date) DO NOTHING
    """, (user_id, today))
    c.execute(f"UPDATE usage_limits SET {field} = {field} + 1 WHERE user_id=? AND date=?", (user_id, today))
    conn.commit()
    conn.close()

def add_clothing(filename, category, color):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO clothes (filename, category, color) VALUES (?, ?, ?)", (filename, category, color))
    conn.commit()
    item_id = c.lastrowid
    conn.close()
    return item_id

def get_all_clothes():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM clothes ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_clothing(item_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM clothes WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
