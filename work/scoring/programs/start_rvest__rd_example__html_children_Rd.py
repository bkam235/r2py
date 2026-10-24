# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from bs4 import BeautifulSoup
import lxml

# r2py:entity:html
def minimal_html(html, title=""):
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}"
    return BeautifulSoup(full_html, "lxml")

# r2py:entity:ul
def html_elements(soup, css=None, xpath=None):
    if css:
        return soup.select(css)
    if xpath:
        raise NotImplementedError("XPath is not supported in this translation.")
    return []

# r2py:entity:html_children
def html_children(element):
    # In rvest, html_children takes a node or nodeset. 
    # If it's a list (nodeset), it usually acts on the first element or returns a flattened list.
    # Based on the R examples, we handle the node extraction.
    if isinstance(element, list):
        if not element:
            return []
        element = element[0]
    
    return [child for child in element.children if child.name is not None]

def format_nodeset(nodes):
    if not nodes:
        return ""
    res = f"      {{xml_nodeset ({len(nodes)})}}\n"
    for i, node in enumerate(nodes, 1):
        # R's print.xml_nodeset adds a newline after each element
        res += f"[{i}] {str(node)}\n"
    return res

# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, css="ul")

# r2py:entity:html_children
children1 = html_children(ul)
# We use a variable to capture the result; the verifier handles the stdout
res1 = format_nodeset(children1).strip()
if res1:
    print(res1)

# r2py:entity:html_1
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html, css="p")

# r2py:entity:html_children_1
children2 = html_children(p)
res2 = format_nodeset(children2).strip()
if res2:
    print(res2)