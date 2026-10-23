from bs4 import BeautifulSoup
import numpy as np

# r2py:entity:html
html_content = """
  <h1>This is a heading</h1>
  <p id='first'>This is a paragraph</p>
  <p class='important'>This is an important paragraph</p>
"""
html = BeautifulSoup(html_content, 'html.parser')

# html |> html_element("h1")
# r2py:entity:html_element
html_element_res = html.select_one("h1")
print(html_element_res)

# html |> html_elements("p")
# r2py:entity:html_elements
html_elements_res = html.select("p")
print(html_elements_res)

# html |> html_elements(".important")
# r2py:entity:html_elements_1
html_elements_res_1 = html.select(".important")
print(html_elements_res_1)

# html |> html_elements("#first")
# r2py:entity:html_elements_2
html_elements_res_2 = html.select("#first")
print(html_elements_res_2)

# html_element() vs html_elements() --------------------------------------
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
# r2py:entity:html_elements_3
li = html.select("li")

# When applied to a node set, html_elements() returns all matching elements
# beneath any of the inputs, flattening results into a new node set.
# li |> html_elements("i")
# r2py:entity:html_elements_4
html_elements_res_4 = []
for node in li:
    html_elements_res_4.extend(node.select("i"))
print(html_elements_res_4)

# When applied to a node set, html_element() always returns a vector the
# same length as the input, using a "missing" element where needed.
# li |> html_element("i")
# r2py:entity:html_element_1
html_element_res_1 = [node.select_one("i") for node in li]
print(html_element_res_1)

# and html_text() and html_attr() will return NA
# li |> html_element("i") |> html_text2()
# r2py:entity:html_element_2
# html_text2 is approximately get_text(strip=True) or just the text
# R's html_text2 handles whitespace and NAs. 
# we represent NA as None in Python lists for these types of operations.
html_text2_res = [node.select_one("i").get_text() if node.select_one("i") else None for node in li]
print(html_text2_res)

# li |> html_element("span") |> html_attr("class")
# r2py:entity:html_element_3
# r2py:entity:html_attr
html_attr_res = [node.select_one("span").get('class')[0] if (node.select_one("span") and node.select_one("span").get('class')) else None for node in li]
print(html_attr_res)