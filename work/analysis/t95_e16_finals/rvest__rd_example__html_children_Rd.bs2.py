# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from bs4 import BeautifulSoup
import lxml

BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "body", "div", "dl",
    "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2",
    "h3", "h4", "h5", "h6", "head", "header", "hr", "html", "li", "main",
    "nav", "ol", "p", "pre", "section", "table", "tbody", "td", "tfoot",
    "th", "thead", "tr", "ul",
}


class XmlDocument:
    def __init__(self, soup, body_text):
        self.soup = soup
        self.body_text = body_text

    def __str__(self):
        return self.body_text

    def __repr__(self):
        return self.body_text


# r2py:entity:html
def minimal_html(html, title=""):
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}"
    soup = BeautifulSoup(full_html, "lxml")
    body = soup.body.decode_contents() if soup.body else ""
    text = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
        "<meta charset=\"utf-8\">\n"
        f"<title>{title}</title>\n"
        "</head>\n"
        f"<body>{body}</body>\n"
        "</html>\n"
    )
    return XmlDocument(soup, text)


# r2py:entity:ul
def html_elements(doc, css=None, xpath=None):
    soup = doc.soup if isinstance(doc, XmlDocument) else doc
    if css:
        return soup.select(css)
    if xpath:
        raise NotImplementedError("XPath is not supported in this translation.")
    return []


# r2py:entity:html_children
def html_children(element):
    if isinstance(element, list):
        if not element:
            return []
        element = element[0]

    return [child for child in element.children if child.name is not None]


def format_nodeset(nodes):
    if not nodes:
        return ""
    res = f"      {{xml_nodeset ({len(nodes)})}}\n"
    n = len(nodes)
    for i, node in enumerate(nodes, 1):
        s = str(node)
        if node.name in BLOCK_TAGS and i < n:
            s += "\\n"
        res += f"[{i}] {s}\n"
    return res


# r2py:entity:html
html = minimal_html("<ul><li>1<li>2<li>3</ul>")
# r2py:entity:ul
ul = html_elements(html, css="ul")

# r2py:entity:html_children
children1 = html_children(ul)
res1 = format_nodeset(children1).strip()
if res1:
    print(res1)

# r2py:entity:html_1
html = minimal_html("<p>Hello <b>Hadley</b><i>!</i>")
# r2py:entity:p
p = html_elements(html, css="p")

# r2py:entity:html_children_1
children2 = html_children(p)
res2 = format_nodeset(children2).strip()
if res2:
    print(res2)