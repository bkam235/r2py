from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# library(rvest) is handled by the imports above

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(func):
    return func

def minimal_html(html_str, title=""):
    # rvest::minimal_html creates a basic HTML structure
    full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{title}</title></head><body>{html_str}</body></html>"
    return BeautifulSoup(full_html, "html.parser")

def html_elements(soup, selector):
    # rvest::html_elements returns a nodeset (list of elements)
    return soup.select(selector)

def html_children(nodeset):
    # rvest::html_children returns the children of the elements in the nodeset
    # If nodeset is a list, it typically returns children of the first element in this context
    if isinstance(nodeset, list):
        if not nodeset:
            return []
        target = nodeset[0]
    else:
        target = nodeset
    
    # Return only Tag objects (exclude NavigableStrings/comments)
    return [child for child in target.children if child.name is not None]

# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, "ul")
# r2py:entity:html_children
html_children_res1 = html_children(ul)

# r2py:entity:html_1
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html, "p")
# r2py:entity:html_children_1
html_children_res2 = html_children(p)