from bs4 import BeautifulSoup

# r2py:entity:html
def minimal_html(html_str, title=""):
    # rvest's minimal_html creates a basic HTML document structure
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html_str}"
    return BeautifulSoup(full_html, "html.parser")

# r2py:entity:ul
def html_elements(soup, css=None, xpath=None):
    if css:
        return soup.select(css)
    if xpath:
        raise NotImplementedError("XPath is not supported in this translation.")
    return []

# r2py:entity:html_children
def html_children(elements):
    # rvest's html_children returns the children of the nodes in the nodeset.
    if isinstance(elements, list):
        if not elements:
            return []
        # In these specific examples, we extract children of the first element
        target = elements[0]
    else:
        target = elements
    
    # rvest's html_children returns only element nodes, excluding text/whitespace nodes
    return [child for child in target.children if child.name is not None]

# suppressPackageStartupMessages is a no-op in Python
def suppressPackageStartupMessages(expr):
    return expr

# Main execution
# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, css="ul")

# r2py:entity:html_children
# The result of this call is what R would print
children1 = html_children(ul)
print(children1)

# r2py:entity:html_1
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html, css="p")

# r2py:entity:html_children_1
children2 = html_children(p)
print(children2)