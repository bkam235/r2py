from bs4 import BeautifulSoup

def minimal_html(html_content):
    # rvest's minimal_html wraps content in basic HTML structure
    return BeautifulSoup(html_content, "html.parser")

def html_elements(html_obj, selector):
    # Return a list of elements matching the selector
    return html_obj.select(selector)

def html_children(elements):
    # If a list of elements is provided, rvest typically operates on the first element
    # or returns the children of the first element in the nodeset.
    target = elements[0] if isinstance(elements, list) and elements else elements
    # Return only Tag objects, excluding NavigableStrings (which rvest's html_children typically does)
    return [child for child in target.children if child.name is not None]

# suppressPackageStartupMessages(library(rvest))
# import_rvest handled by imports above

# html <- minimal_html("<ul><li>1<li>2<li>3</ul>")
html = minimal_html("<ul><li>1<li>2<li>3</ul>")

# ul <- html_elements(html, "ul")
ul = html_elements(html, "ul")

# html_children(ul)
html_children_result1 = html_children(ul)
print(html_children_result1)

# html <- minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")

# p <- html_elements(html, "p")
p = html_elements(html, "p")

# html_children(p)
html_children_result2 = html_children(p)
print(html_children_result2)