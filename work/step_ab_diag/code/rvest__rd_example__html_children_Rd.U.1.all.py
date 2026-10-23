from bs4 import BeautifulSoup

# r2py:entity:import_rvest
# rvest is imported via BeautifulSoup/lxml logic

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(msg):
    pass

def minimal_html(html, title=""):
    # rvest's minimal_html wraps content in a standard HTML shell
    full_html = f"<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n<meta charset=\"utf-8\">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>"
    return BeautifulSoup(full_html, "html.parser")

def html_elements(soup, selector):
    # Returns a list of elements matching the selector
    return soup.select(selector)

def html_children(elements):
    # rvest's html_children returns the immediate children of the first element in the nodeset
    # if a nodeset is provided.
    if isinstance(elements, list):
        if not elements:
            return []
        target = elements[0]
    else:
        target = elements
    
    # We return all children including strings (text nodes), but filter for those 
    # that are effectively "children" in the XML sense.
    # bs4 .children includes NavigableStrings and Tags.
    return list(target.children)

# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, "ul")

# r2py:entity:html_children
# The R script calls html_children(ul) and implicitly prints it
res_children1 = html_children(ul)
print(res_children1)

# r2py:entity:html_1
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html, "p")

# r2py:entity:html_children_1
# The R script calls html_children(p) and implicitly prints it
res_children2 = html_children(p)
print(res_children2)