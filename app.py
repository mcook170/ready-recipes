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
    if request.method == "GET":
        return render_template("add_recipe.html")
    
    url = request.form["url"]

    # Scrape the recipe
    scraped = extract_recipe(url)

    if not scraped or "title" not in scraped:
        return render_template("error.html", message="Could not extract recipe from this URL")

    # Extract fields
    title = scraped.get("title")
    ingredients = scraped.get("ingredients", [])
    instructions = scraped.get("instructions", [])
    image_url = scraped.get("image_url")  # <-- IMPORTANT

    # Combine instructions into a text block (optional)
    content = "\n".join(instructions)

    # Save to database
    save_recipe(
        title=title,
        content=content,
        image_url=image_url,
        ingredients=ingredients,
        instructions=instructions
    )

    return redirect("/")



@app.route("/recipe/<int:id>")
def recipe(id):
    recipe = get_recipe(id)
    print("Loaded Recipe: ", recipe)  # FIXME: Debugging statement
    return render_template("recipe.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
