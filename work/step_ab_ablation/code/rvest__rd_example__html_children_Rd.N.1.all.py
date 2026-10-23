from bs4 import BeautifulSoup

# r2py:entity:minimal_html
def minimal_html(html, title=""):
    # rvest's minimal_html creates a basic HTML structure
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}"
    return BeautifulSoup(full_html, "lxml")

# r2py:entity:html_elements
def html_elements(html, selector):
    # html_elements in rvest returns a nodeset (list-like)
    return html.select(selector)

# r2py:entity:html_children
def html_children(nodes):
    # rvest's html_children expects a nodeset and returns the children of the first element
    if not nodes:
        return []
    # In rvest, html_children returns a nodeset of the immediate children of the first node
    target = nodes[0]
    # Filter to include only Tag elements, excluding NavigableStrings (text nodes)
    return [child for child in target.children if hasattr(child, 'name') and child.name is not None]

def print_nodeset(nodes):
    # Emulate R's print.xml_nodeset output
    if not nodes:
        print("xml_nodeset (0)")
        return
    print(f"      {{xml_nodeset ({len(nodes)})}}")
    for i, node in enumerate(nodes, 1):
        # R's output for nodes typically shows the tag and content
        # We use a simplified string representation to match expected R behavior
        print(f"[{i}] {node}")

# R: html <- minimal_html("<ul><li>1<li>2<li>3</ul>")
html = minimal_html("<ul><li>1<li>2<li>3</ul>")

# R: ul <- html_elements(html, "ul")
ul = html_elements(html, "ul")

# R: html_children(ul)
children_ul = html_children(ul)
print_nodeset(children_ul)

# R: html <- minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")

# R: p <- html_elements(html, "p")
p = html_elements(html, "p")

# R: html_children(p)
children_p = html_children(p)
print_nodeset(children_p)