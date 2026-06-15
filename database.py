import sqlite3
import json

DB_NAME = "tickets.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            embedding TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_ticket(title, description, embedding_vector):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    embedding_json = json.dumps(embedding_vector.tolist())
    cursor.execute('''
        INSERT INTO tickets (title, description, embedding)
        VALUES (?, ?, ?)
    ''', (title, description, embedding_json))
    conn.commit()
    conn.close()

def get_all_tickets():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, embedding FROM tickets")
    rows = cursor.fetchall()
    conn.close()
    
    tickets = []
    for row in rows:
        tickets.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "embedding": json.loads(row[3])
        })
    return tickets