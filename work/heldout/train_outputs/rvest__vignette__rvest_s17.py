# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

from bs4 import BeautifulSoup

# r2py:entity:html
# minimal_html(html, title="") implementation:
# xml2::read_html(paste0("<!doctype html>\n", "<meta charset=utf-8>\n", "<title>", title, "</title>\n", html))
html_content = """
  <ul>
    <li><b>C-3PO</b> is a <i>droid</i> that weighs <span class_val='weight'>167 kg</span></li>
    <li><b>R2-D2</b> is a <i>droid</i> that weighs <span class_val='weight'>96 kg</span></li>
    <li><b>Yoda</b> weighs <span class_val='weight'>66 kg</span></li>
    <li><b>R4-P17</b> is a <i>droid</i></li>
  </ul>
"""
title = ""
full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html_content}"
html = BeautifulSoup(full_html, 'html.parser')