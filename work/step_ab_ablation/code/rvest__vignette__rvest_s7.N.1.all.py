from bs4 import BeautifulSoup

# Helper to mimic rvest::minimal_html
def minimal_html(html, title=""):
    # rvest::minimal_html wraps the snippet in a basic HTML structure
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}"
    return BeautifulSoup(full_html, 'html.parser')

# r2py:entity:html
html = minimal_html("""
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
""")

# R: html |> html_elements("li") |> html_text2()
# r2py:entity:html_elements
elements = html.select("li")

# r2py:entity:html_text2
# html_text2() in rvest returns the text as seen by the user (handles entities, preserves basic spacing)
# In BeautifulSoup, get_text() with strip=True is close, but rvest's html_text2 specifically 
# focuses on the "visual" text content.
html_text2 = [el.get_text(strip=True) for el in elements]

# To match the R pipeline output, we ensure the final result is available
result = html_text2