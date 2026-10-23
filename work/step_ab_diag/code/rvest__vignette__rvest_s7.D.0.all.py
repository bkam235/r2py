from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# suppressPackageStartupMessages(library(rvest)) is handled by imports

# Helper to mimic rvest::minimal_html
def minimal_html(html, title=""):
    # R's minimal_html wraps content in a full HTML structure
    full_html = f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>'
    return full_html

# r2py:entity:html
html_content = """
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
"""
html = minimal_html(html_content)

# To perform operations, we need a BeautifulSoup object
soup = BeautifulSoup(html, 'html.parser')

# r2py:entity:html_elements
# html_elements("li") finds all elements matching the CSS selector
elements = soup.select("li")

# r2py:entity:html_text2
# html_text2() returns a character vector of the text content, 
# mimicking how it strips whitespace and handles entities
result = [el.get_text(strip=True) for el in elements]

# Printing as an R character vector: [1] "apple & pear" "banana" "pineapple"
print(f'[1] { " ".join(f'\"{x}\"' for x in result) }')