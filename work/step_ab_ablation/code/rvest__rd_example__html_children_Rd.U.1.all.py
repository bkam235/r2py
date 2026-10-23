from bs4 import BeautifulSoup

# r2py:entity:minimal_html
def minimal_html(html_string, title=""):
    # rvest's minimal_html creates a full document structure
    full_html = f"<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n<meta charset=\"utf-8\">\n<title>{title}</title>\n</head>\n<body>{html_string}</body>\n</html>"
    return BeautifulSoup(full_html, "html.parser")

# r2py:entity:html_elements
def html_elements(soup, selector):
    # If soup is already a list of elements (xml_nodeset), we return it or filter it
    if isinstance(soup, list):
        return soup
    return soup.select(selector)

# r2py:entity:html_children
def html_children(elements):
    # rvest's html_children returns the immediate children elements (tags) of the nodeset
    if not isinstance(elements, list):
        elements = [elements]
    
    all_children = []
    for el in elements:
        # Only include tags, not NavigableStrings (text)
        children = [child for child in el.children if child.name is not None]
        all_children.extend(children)
    return all_children

# The R script logic
# suppressPackageStartupMessages(library(rvest)) - handled by imports

# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, "ul")
# r2py:entity:html_children
children1 = html_children(ul)
print(children1)

# r2py:entity:html_1
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html, "p")
# r2py:entity:html_children_1
children2 = html_children(p)
print(children2)