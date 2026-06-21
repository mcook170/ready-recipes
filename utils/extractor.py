import requests
import json
import re
from bs4 import BeautifulSoup


def normalize_text(text):
    if not isinstance(text, str):
        return text

    text = text.replace('–', '-').replace('—', '-').replace('·', ' ')

    units = r'(?:tbsp\.?|tsp\.?|tablespoons?|teaspoons?|cups?|ounces?|pounds?|grams?|cloves?|oz\.?|lb\.?|pinch\.?|dash\.?)'

    text = re.sub(r'(\d+(?:\s*/\s*\d+)?)\s*(' + units + r')', r'\1 \2', text, flags=re.IGNORECASE)
    text = re.sub(r'(' + units + r')(?=[A-Za-z])', r'\1 ', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_recipe(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # -----------------------------
    # 1. TRY JSON-LD FIRST
    # -----------------------------
    recipe = None
    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            data = json.loads(script.string)

            # JSON-LD can be a list or dict
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") in ["Recipe", ["Recipe"]]:
                        recipe = item
                        break
            elif isinstance(data, dict):
                if data.get("@type") in ["Recipe", ["Recipe"]]:
                    recipe = data
                    break
        except:
            continue

    if recipe:
        # Extract JSON-LD fields
        title = recipe.get("name", "Untitled Recipe")
        ingredients = [normalize_text(item) for item in recipe.get("recipeIngredient", [])]
        instructions_raw = recipe.get("recipeInstructions", [])

        instructions = []
        for step in instructions_raw:
            if isinstance(step, dict):
                instructions.append(normalize_text(step.get("text", "")))
            else:
                instructions.append(normalize_text(step))

        # Image handling
        image_data = recipe.get("image")
        image_url = None
        if isinstance(image_data, str):
            image_url = image_data
        elif isinstance(image_data, list) and image_data:
            image_url = image_data[0]
        elif isinstance(image_data, dict):
            image_url = image_data.get("url")

        return {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "image_url": image_url
        }

    # -----------------------------
    # 2. HTML FALLBACK SCRAPING
    # -----------------------------
    # Title
    title = soup.find("h1")
    title = title.get_text(strip=True) if title else "Untitled Recipe"

    # Ingredients (common WordPress selectors)
    ingredients = []
    for selector in [
        ".wprm-recipe-ingredient",      # WP Recipe Maker
        ".tasty-recipes-ingredients li",
        ".recipe-ingredients li",
        ".ingredients li",
        ".ingredient"
    ]:
        items = soup.select(selector)
        if items:
            ingredients = [normalize_text(i.get_text(" ", strip=True)) for i in items]
            break

    # Instructions (common selectors)
    instructions = []
    for selector in [
        ".wprm-recipe-instruction",     # WP Recipe Maker
        ".tasty-recipes-instructions li",
        ".recipe-instructions li",
        ".instructions li",
        ".instruction"
    ]:
        steps = soup.select(selector)
        if steps:
            instructions = [normalize_text(s.get_text(" ", strip=True)) for s in steps]
            break

    # Image fallback
    image_url = None
    og_image = soup.find("meta", property="og:image")
    if og_image:
        image_url = og_image.get("content")

    # If we found nothing meaningful, return None
    if not ingredients and not instructions:
        return None

    return {
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions,
        "image_url": image_url
    }
