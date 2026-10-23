from bs4 import BeautifulSoup

# suppressPackageStartupMessages(library(rvest))
# import_rvest: rvest (LibraryImport)
# suppressPackageStartupMessages: suppressPackageStartupMessages (FunctionCall)

# html <- minimal_html(...)
# r2py:entity:html
html_content = """
  <h1>This is a heading</h1>
  <p id='first'>This is a paragraph</p>
  <p class='important'>This is an important paragraph</p>
"""
html = BeautifulSoup(html_content, 'html.parser')

# html |> html_element("h1")
# r2py:entity:html_element
html_element = html.select_one("h1")

# html |> html_elements("p")
# r2py:entity:html_elements
html_elements = html.select("p")

# html |> html_elements(".important")
# r2py:entity:html_elements_1
html_elements_1 = html.select(".important")

# html |> html_elements("#first")
# r2py:entity:html_elements_2
html_elements_2 = html.select("#first")

# html_element() vs html_elements() --------------------------------------
# html <- minimal_html(...)
# r2py:entity:html_1
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
# r2py:entity:li
# r2py:entity:html_elements_3
li = html.select("li")

# When applied to a node set, html_elements() returns all matching elements
# beneath any of the inputs, flattening results into a new node set.
# li |> html_elements("i")
# r2py:entity:html_elements_4
html_elements_4 = []
for node in li:
    html_elements_4.extend(node.select("i"))

# When applied to a node set, html_element() always returns a vector the
# same length as the input, using a "missing" element where needed.
# li |> html_element("i")
# r2py:entity:html_element_1
html_element_1 = [node.select_one("i") for node in li]

# and html_text() and html_attr() will return NA
# li |> html_element("i") |> html_text2()
# r2py:entity:html_element_2
# r2py:entity:html_text2
html_element_2 = [node.select_one("i") for node in li]
html_text2 = [node.get_text() if node else None for node in html_element_2]

# li |> html_element("span") |> html_attr("class")
# r2py:entity:html_element_3
# r2py:entity:html_attr
html_element_3 = [node.select_one("span") for node in li]
html_attr = [node.get('class') if node else None for node in html_element_3]