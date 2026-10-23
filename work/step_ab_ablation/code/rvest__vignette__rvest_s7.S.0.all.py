# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# rvest is handled by BeautifulSoup

# r2py:entity:suppressPackageStartupMessages
# No equivalent needed in Python

# r2py:entity:html
# minimal_html creates a simple HTML document structure
html_content = """
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
"""
# mimicking minimal_html by wrapping in basic structure and parsing
html = BeautifulSoup(f"<!doctype html>\n<meta charset=utf-8>\n{html_content}", 'html.parser')

# r2py:entity:html_elements
# html_elements("li") selects all <li> elements
elements = html.select("li")

# r2py:entity:html_text2
# html_text2() extracts text, handles entities, and cleans whitespace
# In R, html_text2 is applied to the result of html_elements
result = [el.get_text(strip=True) for el in elements]