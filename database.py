import sqlite3
import json

# -----------------------------
# CONNECT
# -----------------------------
def connect():
    return sqlite3.connect("recipes.db")


# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image_url TEXT,
            ingredients TEXT,
            instructions TEXT,
            notes TEXT,
            category TEXT,
            is_favorite INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# SAVE RECIPE (URL or Manual)
# -----------------------------
def save_recipe(title, image_url, ingredients, instructions, notes="", category=None):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO recipes (title, image_url, ingredients, instructions, notes, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        image_url,
        json.dumps(ingredients),
        json.dumps(instructions),
        notes,
        category
    ))

    conn.commit()
    conn.close()


# -----------------------------
# GET ALL RECIPES
# -----------------------------
def get_all_recipes():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, image_url, ingredients, instructions, notes, is_favorite
        FROM recipes
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


# -----------------------------
# GET FAVORITED RECIPES
# -----------------------------
def get_favorited_recipes():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, image_url, ingredients, instructions, notes, is_favorite
        FROM recipes
        WHERE is_favorite = 1
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


# -----------------------------
# GET SINGLE RECIPE (dict)
# -----------------------------
def get_recipe(recipe_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, image_url, ingredients, instructions, notes, is_favorite, category
        FROM recipes
        WHERE id = ?
    """, (recipe_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    id, title, image_url, ingredients_json, instructions_json, notes, is_favorite, category = row

    ingredients = json.loads(ingredients_json) if ingredients_json else []
    instructions = json.loads(instructions_json) if instructions_json else []

    return {
        "id": id,
        "title": title,
        "image_url": image_url,
        "ingredients": ingredients,
        "instructions": instructions,
        "notes": notes or "",
        "category": category or "",
        "is_favorite": is_favorite
    }


# -----------------------------
# UPDATE NOTES
# -----------------------------
def update_notes(recipe_id, notes):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE recipes
        SET notes = ?
        WHERE id = ?
    """, (notes, recipe_id))

    conn.commit()
    conn.close()


# -----------------------------
# SEARCH RECIPES
# -----------------------------
def search_recipes(query):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, image_url, ingredients, instructions, notes, is_favorite
        FROM recipes
        WHERE title LIKE ?
        ORDER BY id DESC
    """, (f"%{query}%",))

    rows = cur.fetchall()
    conn.close()
    return rows


# Initialize DB on import
init_db()
