import requests
from readability import Document
from bs4 import BeautifulSoup

def extract_recipe(url):
    response = requests.get(url)
    html = response.text

    # Use Firefox Reader Mode engine
    doc = Document(html)
    title = doc.short_title()
    cleaned_html = doc.summary()

    # Parse cleaned HTML
    soup = BeautifulSoup(cleaned_html, "html.parser")
    text = soup.get_text("\n")

    return {
        "title": title,
        "content": text
    }
