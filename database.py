import sqlite3

def connect():
    return sqlite3.connect("recipes.db")

def save_recipe(title, content):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO recipes (title, content) VALUES (?, ?)",
        (title, content)
    )
    conn.commit()
    recipe_id = cur.lastrowid
    conn.close()
    return recipe_id

def get_all_recipes():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM recipes")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_recipe(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT title, content FROM recipes WHERE id = ?", (id,))
    row = cur.fetchone()
    conn.close()
    return row

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
);
