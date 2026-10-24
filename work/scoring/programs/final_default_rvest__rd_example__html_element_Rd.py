from bs4 import BeautifulSoup

# r2py:data_shim managed by the harness
def minimal_html(html, title=""):
    full_html = f'<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}'
    return BeautifulSoup(full_html, 'html.parser')

def main():
    # r2py:entity:html
    html_content = """
  <h1>This is a heading</h1>
  <p id='first'>This is a paragraph</p>
  <p class='important'>This is an important paragraph</p>
"""
    html = minimal_html(html_content)

    # html |> html_element("h1")
    # r2py:entity:html_element
    res_html_element = html.select_one("h1")
    print(res_html_element)

    # html |> html_elements("p")
    # r2py:entity:html_elements
    res_html_elements = html.select("p")
    print(res_html_elements)

    # html |> html_elements(".important")
    # r2py:entity:html_elements_1
    res_html_elements_1 = html.select(".important")
    print(res_html_elements_1)

    # html |> html_elements("#first")
    # r2py:entity:html_elements_2
    res_html_elements_2 = html.select("#first")
    print(res_html_elements_2)

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
    html = minimal_html(html_content_2)
    # r2py:entity:html_elements_3
    li = html.select("li")

    # When applied to a node set, html_elements() returns all matching elements
    # beneath any of the inputs, flattening results into a new node set.
    # li |> html_elements("i")
    # r2py:entity:html_elements_4
    res_html_elements_4 = []
    for node in li:
        res_html_elements_4.extend(node.select("i"))
    print(res_html_elements_4)

    # When applied to a node set, html_element() always returns a vector the
    # same length as the input, using a "missing" element where needed.
    # li |> html_element("i")
    # r2py:entity:html_element_1
    res_html_element_1 = [node.select_one("i") for node in li]
    print(res_html_element_1)

    # and html_text() and html_attr() will return NA
    # li |> html_element("i") |> html_text2()
    # r2py:entity:html_element_2
    # r2py:entity:html_text2
    res_html_text2 = [node.get_text() if node else None for node in res_html_element_1]
    print(res_html_text2)

    # li |> html_element("span") |> html_attr("class")
    # r2py:entity:html_element_3
    # r2py:entity:html_attr
    res_html_element_3 = [node.select_one("span") for node in li]
    res_html_attr = [node.get('class')[0] if (node and node.has_attr('class')) else None for node in res_html_element_3]
    print(res_html_attr)

if __name__ == "__main__":
    main()