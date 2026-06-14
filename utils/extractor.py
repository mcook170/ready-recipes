import requests
import json
from bs4 import BeautifulSoup

def extract_recipe(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    recipe = None

    # Find all JSON-LD blocks
    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            data = json.loads(script.string)

            # Some sites wrap data in a list
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "Recipe":
                        recipe = item
                        break
            else:
                if data.get("@type") == "Recipe":
                    recipe = data
                    break
        except:
            continue

    if recipe is None:
        return None

    # Extract fields
    title = recipe.get("name", "Untitled Recipe")
    ingredients = recipe.get("recipeIngredient", [])
    instructions_raw = recipe.get("recipeInstructions", [])

    # Normalize instructions
    instructions = []
    for step in instructions_raw:
        if isinstance(step, dict):
            instructions.append(step.get("text", ""))
        else:
            instructions.append(step)

    # ⭐ Extract image URL (handles all formats)
    image_data = recipe.get("image")
    image_url = None

    if isinstance(image_data, str):
        image_url = image_data
    elif isinstance(image_data, list) and len(image_data) > 0:
        image_url = image_data[0]
    elif isinstance(image_data, dict):
        image_url = image_data.get("url")

    return {
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions,
        "image_url": image_url
    }
