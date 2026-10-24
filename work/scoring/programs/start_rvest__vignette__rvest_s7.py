# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

from bs4 import BeautifulSoup

# Helper to mimic rvest::minimal_html
# r2py:entity:html
def minimal_html(html, title=""):
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}"
    return BeautifulSoup(full_html, 'html.parser')

# R's minimal_html returns a parsed document object
html = minimal_html("""
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
""")

# html_elements("li") finds all elements matching the CSS selector
# r2py:entity:html_elements
elements = html.select("li")

# html_text2() returns a character vector of the text content
# it handles entities and strips whitespace
# r2py:entity:html_text2
result = [el.get_text(strip=True) for el in elements]

print(result)