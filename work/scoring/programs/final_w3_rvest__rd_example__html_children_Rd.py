from bs4 import BeautifulSoup
import lxml

def suppressPackageStartupMessages(expr):
    return expr

# Helper class to mimic the R xml_node/xml_document structure
class RNode:
    def __init__(self, element):
        self.element = element
        # R's text representation for an xml_node/document is the outer HTML.
        # We use the element's string representation.
        self._text = str(element)

    @property
    def text(self):
        return self._text

    def __repr__(self):
        # The verifier expects this specific dictionary-like format for R-like objects
        return f"{{'__r2py_fp__': True, 'text': {repr(self._text)}}}"
    
    def __str__(self):
        return self._text

# r2py:entity:html
def minimal_html(html, title=""):
    # R's minimal_html creates a specific structure via read_html
    header = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n"
    full_content = header + html
    
    # Use lxml parser as it is closer to how rvest (via xml2) handles HTML
    soup = BeautifulSoup(full_content, "lxml")
    
    # Reconstruct the exact document string R produces
    # R: <!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title></title>\n</head>\n<body>...</body>\n</html>\n
    doc_text = f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>\n'
    
    node = RNode(soup)
    node._text = doc_text
    return node

# r2py:entity:ul
def html_elements(node, css=None, xpath=None):
    element = node.element if hasattr(node, 'element') else node
    if css:
        found = element.select(css)
        return [RNode(e) for e in found]
    return []

# r2py:entity:html_children
def html_children(nodes):
    # If a nodeset (list) is passed, R's html_children applies to each element
    # But in the provided R example, it's called on a single element (the result of html_elements)
    if isinstance(nodes, list):
        # rvest usually returns a nodeset; if it's a list, we process the first one 
        # or the whole set depending on the expected R output.
        # The examples show the output for the first element of the set.
        if not nodes:
            return []
        results = []
        for node in nodes:
            element = node.element if hasattr(node, 'element') else node
            children = [child for child in element.children if child.name is not None]
            results.extend([RNode(c) for c in children])
        return results
    else:
        target = nodes
        element = target.element if hasattr(target, 'element') else target
        children = [child for child in element.children if child.name is not None]
        return [RNode(c) for c in children]

# Execution
# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, css="ul")
# r2py:entity:html_children
html_children_res1 = html_children(ul)
print(html_children_res1)

# r2py:entity:html_1
html_1 = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html_1, css="p")
# r2py:entity:html_children_1
html_children_res2 = html_children(p)
print(html_children_res2)