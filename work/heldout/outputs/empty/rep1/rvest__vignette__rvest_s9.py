# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import bs4

# r2py:entity:html
def minimal_html(html, title=""):
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}"
    return bs4.BeautifulSoup(full_html, "html.parser")

html = minimal_html("<body>\n  <p>\n  This is\n  a\n  paragraph.</p><p>This is another paragraph.\n  \n  It has two sentences.</p>\n")