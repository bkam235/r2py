from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# In Python, BeautifulSoup is the primary tool for rvest-like functionality.

# r2py:entity:suppressPackageStartupMessages
# This is a no-op in Python.

# r2py:entity:html
def minimal_html(html_content):
    # rvest::minimal_html produces a specific wrapper.
    # We replicate the structure seen in the R output comparison.
    full_html = f"<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n<meta charset=\"utf-8\">\n<title></title>\n</head>\n<body>{html_content}</body>\n</html>"
    return BeautifulSoup(full_html, 'html.parser')

html = minimal_html("""
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
""")

# r2py:entity:html_elements
# Translate: html |> html_elements("li")
html_elements = html.select("li")

# r2py:entity:html_text2
# Translate: html_elements |> html_text2()
# html_text2() returns the text content of each node in a character vector.
html_text2 = [el.get_text() for el in html_elements]

# The final result is printed to match R's autoprint behavior
print(html_text2)