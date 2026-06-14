from flask import Flask, render_template, request, redirect
from utils.extractor import extract_recipe
from database import save_recipe, get_all_recipes, get_recipe

app = Flask(__name__)

@app.route("/")
def index():
    recipes = get_all_recipes()
    return render_template("index.html", recipes=recipes)

@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        url = request.form["url"]
        data = extract_recipe(url)
        recipe_id = save_recipe(data["title"], data["content"])
        return redirect(f"/recipe/{recipe_id}")
    return render_template("add_recipe.html")

@app.route("/recipe/<int:id>")
def recipe(id):
    recipe = get_recipe(id)
    return render_template("recipe.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
