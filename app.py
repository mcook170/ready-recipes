from flask import Flask, render_template, request, redirect
import sqlite3
import json
from utils.extractor import extract_recipe, normalize_text   # your existing scraper
import database as db               # your database.py

app = Flask(__name__)


@app.template_filter('fix_spacing')
def fix_spacing(value):
    return normalize_text(value)


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def index():
    recipes = db.get_all_recipes()
    favorites = db.get_favorited_recipes()
    return render_template("index.html", recipes=recipes, favorites=favorites, search_query=None)


# -----------------------------
# SEARCH
# -----------------------------
@app.get("/search")
def search():
    q = request.args.get("q", "")
    results = db.search_recipes(q)
    favorites = db.get_favorited_recipes()

    return render_template(
        "index.html",
        recipes=results,
        favorites=favorites,
        search_query=q
    )


# -----------------------------
# VIEW SINGLE RECIPE
# -----------------------------
@app.route("/recipe/<int:id>")
def recipe(id):
    recipe = db.get_recipe(id)
    return render_template("recipe.html", recipe=recipe)


# -----------------------------
# FAVORITE TOGGLE
# -----------------------------
@app.post("/favorite/<int:id>")
def favorite(id):
    conn = sqlite3.connect("recipes.db")
    cur = conn.cursor()

    cur.execute("UPDATE recipes SET is_favorite = 1 - is_favorite WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(f"/recipe/{id}")


# -----------------------------
# ADD RECIPE — URL IMPORT
# -----------------------------
@app.post("/add")
def add_recipe():
    url = request.form.get("url")

    if not url:
        return redirect("/add_recipe")

    scraped = extract_recipe(url)

    if scraped is None:
        return "Error: Could not scrape recipe."

    title = scraped.get("title")
    image_url = scraped.get("image_url")
    ingredients = scraped.get("ingredients", [])
    instructions = scraped.get("instructions", [])

    db.save_recipe(title, image_url, ingredients, instructions)

    return redirect("/")


# -----------------------------
# ADD RECIPE — MANUAL ENTRY
# -----------------------------
@app.post("/add_manual")
def add_manual():
    title = request.form.get("title")
    image_url = request.form.get("image_url")
    ingredients = request.form.get("ingredients", "").split("\n")
    instructions = request.form.get("instructions", "").split("\n")
    category = request.form.get("category")
    notes = request.form.get("notes", "")
    db.save_recipe(title, image_url, ingredients, instructions, notes, category)
    return redirect("/")


# -----------------------------
# ADD RECIPE PAGE
# -----------------------------
@app.route("/add_recipe")
def add_recipe_page():
    return render_template("add_recipe.html")

# -----------------------------
# UPDATE NOTES
# -----------------------------
@app.post("/update_notes/<int:id>")
def update_notes(id):
    notes = request.form.get("notes", "")
    db.update_notes(id, notes)
    return redirect(f"/recipe/{id}")

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
