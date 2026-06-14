import sqlite3
import json

def connect():
    return sqlite3.connect("recipes.db")

def init_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image_uDrl TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_recipe(title, content, image_url, ingredients, instructions):
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO recipes (title, content, image_url, ingredients, instructions)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        content,
        image_url,
        json.dumps(ingredients),      # store list as JSON
        json.dumps(instructions)      # store list as JSON
    ))

    conn.commit()
    conn.close()

def get_all_recipes():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM recipes")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_recipe(recipe_id):
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, content, image_url, ingredients, instructions
        FROM recipes
        WHERE id = ?
    """, (recipe_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    title, content, image_url, ingredients_json, instructions_json = row

    # Convert JSON strings back into Python lists
    ingredients = json.loads(ingredients_json) if ingredients_json else []
    instructions = json.loads(instructions_json) if instructions_json else []

    return {
        "title": title,
        "content": content,
        "image_url": image_url,
        "ingredients": ingredients,
        "instructions": instructions
    }

init_db()

