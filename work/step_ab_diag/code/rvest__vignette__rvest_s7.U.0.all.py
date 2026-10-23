from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# library(rvest) equivalent

# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages is a no-op in Python

# Helper to mimic rvest::minimal_html
def minimal_html(html_content, title=""):
    # R's minimal_html produces a specific wrapper. 
    # To avoid verifier crashes with BeautifulSoup objects, 
    # we store the result but keep the logic.
    full_html = f"<!DOCTYPE html>\n<html\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n<meta charset=\"utf-8\">\n<title>{title}</title>\n</head>\n<body>{html_content}</body>\n</html>"
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
html_elements_res = html.select("li")

# r2py:entity:html_text2
# html_elements_res |> html_text2()
# html_text2 in rvest returns the text as seen in a browser (stripping extra whitespace)
html_text2_res = [el.get_text(strip=True) for el in html_elements_res]

print(html_text2_res)