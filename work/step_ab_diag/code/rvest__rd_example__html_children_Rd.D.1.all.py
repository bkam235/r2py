from bs4 import BeautifulSoup

# The R minimal_html function wraps the input in a full HTML structure.
def minimal_html(html, title=""):
    # Based on the verification result, R's minimal_html output is:
    # <!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title></title>\n</head>\n<body...
    full_html = (
        f'<!DOCTYPE html>\n<html>\n<head>\n'
        f'<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
        f'<meta charset="utf-8">\n'
        f'<title>{title}</title>\n'
        f'</head>\n<body>{html}</body>\n</html>'
    )
    # Using 'html.parser' to ensure it runs in most environments without extra binary deps
    return BeautifulSoup(full_html, "html.parser")

def html_elements(soup, selector):
    # rvest::html_elements returns a nodeset (list)
    return soup.select(selector)

def html_children(elements):
    # rvest::html_children takes a nodeset/node and returns the children of the first node.
    # In Python, soup.select returns a list.
    if isinstance(elements, list):
        if not elements:
            return []
        node = elements[0]
    else:
        node = elements
    
    # html_children returns element children, skipping text nodes.
    # find_all(recursive=False) gets only direct child tags.
    return node.find_all(recursive=False)

# suppressPackageStartupMessages(library(rvest))
# Handled by the functions defined above.

# html <- minimal_html("<ul><li>1<li>2<li>3</ul>")
html = minimal_html("<ul><li>1<li>2<li>3</ul>")

# ul <- html_elements(html, "ul")
ul = html_elements(html, "ul")

# html_children(ul)
html_children_val = html_children(ul)

# html <- minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")

# p <- html_elements(html, "p")
p = html_elements(html, "p")

# html_children(p)
html_children_val_1 = html_children(p)