from bs4 import BeautifulSoup

# r2py:entity:html
def minimal_html(html_content, title=""):
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html_content}"
    return BeautifulSoup(full_html, "lxml")

# r2py:entity:ul
def html_elements(soup, selector):
    # rvest::html_elements returns a nodeset (list of elements)
    if isinstance(soup, BeautifulSoup):
        return soup.select(selector)
    elif isinstance(soup, list):
        # If soup is already a list of elements, we search within them
        results = []
        for item in soup:
            results.extend(item.select(selector))
        return results
    return []

# r2py:entity:html_children
def html_children(nodes):
    # rvest::html_children returns children of the first node in the nodeset
    if not nodes:
        return []
    
    # Handle nodeset (list) or single element
    target = nodes[0] if isinstance(nodes, list) else nodes
    
    # Return only Tag objects (skip NavigableStrings/Comments to match xml2 behavior)
    return [child for child in target.children if child.name is not None]

# suppressPackageStartupMessages(library(rvest))
# (Implicitly handled by imports)

# html <- minimal_html("<ul><li>1<li>2<li>3</ul>")
html = minimal_html("<ul><li>1<li>2<li>3</ul>")

# ul <- html_elements(html, "ul")
ul = html_elements(html, "ul")

# html_children(ul)
html_children_result = html_children(ul)
print(html_children_result)

# html <- minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")

# p <- html_elements(html, "p")
p = html_elements(html, "p")

# html_children(p)
html_children_result_2 = html_children(p)
print(html_children_result_2)