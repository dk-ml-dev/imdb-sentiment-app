import sqlite3
from datetime import datetime
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Database path
DB_PATH = "data/IMDb_Sentiment.db"

# Create the reviews table
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original TEXT,
        translated TEXT,
        sentiment TEXT,
        score REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# Insert a new review
def insert_review(original, translated, sentiment, score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO reviews (original, translated, sentiment, score)
    VALUES (?, ?, ?, ?)
    """, (original, translated, sentiment, score))
    conn.commit()
    conn.close()

# Fetch recent reviews
def fetch_reviews(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT original, translated, sentiment, score, timestamp
    FROM reviews
    ORDER BY timestamp DESC
    LIMIT ?
    """, (limit,))
    results = cursor.fetchall()
    conn.close()
    return results