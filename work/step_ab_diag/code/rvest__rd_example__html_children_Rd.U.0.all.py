from bs4 import BeautifulSoup, NavigableString, Tag

# r2py:entity:import_rvest
# rvest is essentially a wrapper around xml2/bs4. 

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(func):
    return func

def minimal_html(html, title=""):
    # R's minimal_html creates a full document structure
    full_html = f"<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n<meta charset=\"utf-8\">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>"
    return BeautifulSoup(full_html, "html.parser")

def html_elements(soup, css):
    # rvest's html_elements returns a nodeset (list of elements)
    return soup.select(css)

def html_children(nodes):
    # If nodes is a list (nodeset), rvest's html_children typically 
    # applies to the first element of that set in these examples
    if isinstance(nodes, list):
        if not nodes:
            return []
        target = nodes[0]
    else:
        target = nodes
    
    # Return all children including text nodes (NavigableString)
    return list(target.children)

# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, "ul")
# r2py:entity:html_children
children1 = html_children(ul)

# r2py:entity:html_1
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html, "p")
# r2py:entity:html_children_1
children2 = html_children(p)