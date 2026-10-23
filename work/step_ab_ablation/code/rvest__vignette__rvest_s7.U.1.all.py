from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# Equivalent to library(rvest)

# r2py:entity:suppressPackageStartupMessages
# No-op in Python

# Helper to mimic rvest::minimal_html
def minimal_html(html_content, title=""):
    # rvest::minimal_html creates a full HTML document structure
    full_html = f"<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n<meta charset=\"utf-8\">\n<title>{title}</title>\n</head>\n<body>{html_content}</body>\n</html>"
    return BeautifulSoup(full_html, 'html.parser')

# r2py:entity:html
html = minimal_html("""
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
""")

# r2py:entity:html_elements
# html |> html_elements("li")
html_elements_result = html.select("li")

# r2py:entity:html_text2
# html_text2() returns text, handles entities, and strips leading/trailing whitespace
html_text2_result = [el.get_text(strip=True) for el in html_elements_result]

# Assign the final result to a variable that would be printed by R
# The pipeline result in R is the output of html_text2()
print(html_text2_result)