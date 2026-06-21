import sqlite3

from database import connect

def add_favorite_column():
    conn = connect()
    cur = conn.cursor()
    cur.execute("ALTER TABLE recipes ADD COLUMN category TEXT")
    conn.commit()
    conn.close()

add_favorite_column()
