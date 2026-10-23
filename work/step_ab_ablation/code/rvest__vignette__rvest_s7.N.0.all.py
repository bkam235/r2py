# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

from bs4 import BeautifulSoup

# Helper to mimic rvest::minimal_html
# r2py:entity:html
def minimal_html(html_content, title=""):
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html_content}"
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
def html_elements(soup, selector):
    return soup.select(selector)

elements = html_elements(html, "li")

# html_text2() returns a character vector of the text content
# It behaves like the browser's innerText, which handles whitespace and entities
# r2py:entity:html_text2
def html_text2(elements):
    # BeautifulSoup's get_text() handles entities automatically.
    # html_text2 in rvest trims leading/trailing whitespace from the final string
    # but preserves internal formatting.
    return [el.get_text().strip() for el in elements]

result = html_text2(elements)