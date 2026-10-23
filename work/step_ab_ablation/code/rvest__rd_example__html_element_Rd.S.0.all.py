from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# rvest is simulated via BeautifulSoup

def minimal_html(html_string):
    return BeautifulSoup(html_string, 'html.parser')

def html_element(node, selector):
    if hasattr(node, 'select_one'):
        return node.select_one(selector)
    # If node is a list (node set)
    return [n.select_one(selector) for n in node]

def html_elements(node, selector):
    if hasattr(node, 'select'):
        return node.select(selector)
    # If node is a list (node set), flatten results
    results = []
    for n in node:
        results.extend(n.select(selector))
    return results

def html_text2(nodes):
    if nodes is None:
        return None
    if isinstance(nodes, list):
        return [n.get_text(strip=True) if n is not None else None for n in nodes]
    return nodes.get_text(strip=True)

def html_attr(nodes, attr):
    if nodes is None:
        return None
    if isinstance(nodes, list):
        return [n.get(attr) if n is not None else None for n in nodes]
    return nodes.get(attr)

# suppressPackageStartupMessages is a no-op in Python
def suppressPackageStartupMessages(expr):
    return expr

# r2py:entity:html
html = minimal_html("
  <h1>This is a heading</h1>
  <p id='first'>This is a paragraph</p>
  <p class='important'>This is an important paragraph</p>
")

# html |> html_element("h1")
# r2py:entity:html_element
html_element_res = html_element(html, "h1")

# html |> html_elements("p")
# r2py:entity:html_elements
html_elements_res = html_elements(html, "p")

# html |> html_elements(".important")
# r2py:entity:html_elements_1
html_elements_res_1 = html_elements(html, ".important")

# html |> html_elements("#first")
# r2py:entity:html_elements_2
html_elements_res_2 = html_elements(html, "#first")

# html_element() vs html_elements() --------------------------------------
# r2py:entity:html_1
html = minimal_html("
  <ul>
    <li><b>C-3PO</b> is a <i>droid</i> that weighs <span class='weight'>167 kg</span></li>
    <li><b>R2-D2</b> is a <i>droid</i> that weighs <span class='weight'>96 kg</span></li>
    <li><b>Yoda</b> weighs <span class='weight'>66 kg</span></li>
    <li><b>R4-P17</b> is a <i>droid</i></li>
  </ul>
")

# r2py:entity:li
li = html_elements(html, "li")

# When applied to a node set, html_elements() returns all matching elements
# beneath any of the inputs, flattening results into a new node set.
# r2py:entity:html_elements_4
li_i_elements = html_elements(li, "i")

# When applied to a node set, html_element() always returns a vector the
# same length as the input, using a "missing" element where needed.
# r2py:entity:html_element_1
li_i_element = html_element(li, "i")

# and html_text() and html_attr() will return NA
# r2py:entity:html_text2
# li |> html_element("i") |> html_text2()
li_i_text = html_text2(html_element(li, "i"))

# r2py:entity:html_attr
# li |> html_element("span") |> html_attr("class")
li_span_class = html_attr(html_element(li, "span"), "class")