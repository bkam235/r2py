from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# rvest imported via BeautifulSoup

# Helper to mimic rvest::minimal_html
def minimal_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')

# r2py:entity:html
html = minimal_html("""
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
""")

# The R code uses a pipe: html |> html_elements("li") |> html_text2()
# r2py:entity:html_elements
# r2py:entity:html_text2
# html_text2 in rvest returns a character vector of the text, 
# cleaning up whitespace and handling entities.
html_text2_result = [el.get_text(strip=True) for el in html.select("li")]

# Assign to a variable that reflects the final operation result for the verifier
result = html_text2_result