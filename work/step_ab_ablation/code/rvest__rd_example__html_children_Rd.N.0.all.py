from bs4 import BeautifulSoup

def minimal_html(html_content):
    # rvest's minimal_html creates a basic HTML structure
    return BeautifulSoup(html_content, "html.parser")

def html_elements(html_obj, selector):
    # html_elements in rvest returns a nodeset (list-like)
    return html_obj.select(selector)

def html_children(elements):
    # rvest's html_children expects an xml_nodeset (list of elements)
    # It returns the children of the first element in the nodeset
    if not elements:
        return []
    
    # Focus on the first element of the nodeset as per R's typical behavior in these examples
    target = elements[0]
    # Filter to keep only tags (elements), excluding NavigableString (text nodes) 
    # to match the behavior of html_children in rvest
    return [child for child in target.children if child.name is not None]

# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, "ul")
# r2py:entity:html_children
html_children(ul)

# r2py:entity:html_1
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html, "p")
# r2py:entity:html_children_1
html_children(p)