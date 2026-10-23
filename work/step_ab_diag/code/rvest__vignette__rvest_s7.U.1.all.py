from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# No direct equivalent for suppressPackageStartupMessages in Python

# r2py:entity:html
def minimal_html(html_content, title=""):
    # rvest::minimal_html creates a full HTML document structure
    return f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html_content}</body>\n</html>'

html = minimal_html("""
  <ol>
    <li>apple &amp; pear</li>
    <li>banana</li>
    <li>pineapple</li>
  </ol>
""")

# r2py:entity:html_elements
def html_elements(html_obj, selector):
    soup = BeautifulSoup(html_obj, 'html.parser')
    return soup.select(selector)

# r2py:entity:html_text2
def html_text2(elements):
    # html_text2 in rvest returns a vector of text, 
    # it handles entities and simplifies whitespace
    return [el.get_text(strip=True) for el in elements]

# Mimicking the pipeline: html |> html_elements("li") |> html_text2()
elements = html_elements(html, "li")
result = html_text2(elements)

print(result)