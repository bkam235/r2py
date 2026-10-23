from bs4 import BeautifulSoup

# r2py:data_shim managed by the harness
# The R original uses minimal_html, which creates a basic HTML document.
# In Python, BeautifulSoup handles this.

# html <- minimal_html(...)
html_content = """
  <h1>This is a heading</h1>
  <p id='first'>This is a paragraph</p>
  <p class='important'>This is an important paragraph</p>
"""
html = BeautifulSoup(html_content, 'html.parser')

# html |> html_element("h1")
html_element = html.select_one("h1")

# html |> html_elements("p")
html_elements = html.select("p")

# html |> html_elements(".important")
html_elements_1 = html.select(".important")

# html |> html_elements("#first")
html_elements_2 = html.select("#first")

# html_element() vs html_elements() --------------------------------------
# html <- minimal_html(...)
html_content_2 = """
  <ul>
    <li><b>C-3PO</b> is a <i>droid</i> that weighs <span class='weight'>167 kg</span></li>
    <li><b>R2-D2</b> is a <i>droid</i> that weighs <span class='weight'>96 kg</span></li>
    <li><b>Yoda</b> weighs <span class='weight'>66 kg</span></li>
    <li><b>R4-P17</b> is a <i>droid</i></li>
  </ul>
"""
html = BeautifulSoup(html_content_2, 'html.parser')

# li <- html |> html_elements("li")
li = html.select("li")

# When applied to a node set, html_elements() returns all matching elements
# beneath any of the inputs, flattening results into a new node set.
# li |> html_elements("i")
html_elements_4 = []
for node in li:
    html_elements_4.extend(node.select("i"))

# When applied to a node set, html_element() always returns a vector the
# same length as the input, using a "missing" element where needed.
# li |> html_element("i")
html_element_1 = [node.select_one("i") for node in li]

# and html_text() and html_attr() will return NA
# li |> html_element("i") |> html_text2()
html_text2 = [node.select_one("i").get_text(strip=True) if node.select_one("i") else None for node in li]

# li |> html_element("span") |> html_attr("class")
html_attr = [node.select_one("span").get('class') if node.select_one("span") else None for node in li]