from bs4 import BeautifulSoup

# r2py:entity:html
html_content = """
  <h1>This is a heading</h1>
  <p id='first'>This is a paragraph</p>
  <p class='important'>This is an important paragraph</p>
"""
html = BeautifulSoup(html_content, 'html.parser')

# html |> html_element("h1")
# r2py:entity:html_element
print(html.select_one("h1"))

# html |> html_elements("p")
# r2py:entity:html_elements
print(html.select("p"))

# html |> html_elements(".important")
# r2py:entity:html_elements_1
print(html.select(".important"))

# html |> html_elements("#first")
# r2py:entity:html_elements_2
print(html.select("#first"))

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
all_i = []
for item in li:
    all_i.extend(item.select("i"))
print(all_i)

# When applied to a node set, html_element() always returns a vector the
# same length as the input, using a "missing" element where needed.
# li |> html_element("i")
# r2py:entity:html_element_1
first_i_per_li = [item.select_one("i") for item in li]
print(first_i_per_li)

# and html_text() and html_attr() will return NA
# li |> html_element("i") |> html_text2()
# r2py:entity:html_element_2
# r2py:entity:html_text2
first_i_text = [item.select_one("i").get_text(strip=True) if item.select_one("i") else None for item in li]
print(first_i_text)

# li |> html_element("span") |> html_attr("class")
# r2py:entity:html_element_3
# r2py:entity:html_attr
span_class = [item.select_one("span").get('class')[0] if (item.select_one("span") and item.select_one("span").get('class')) else None for item in li]
print(span_class)