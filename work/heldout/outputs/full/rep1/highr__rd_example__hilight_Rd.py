# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, LatexFormatter

# Simulation of highr's internal markup data frames
# highr:::cmd_latex and highr:::cmd_html are data frames defining colors/styles
cmd_latex = pd.DataFrame({"start": ["\\color{blue}"], "end": ["\\color{black}"]}, index=["DEFAULT"])
cmd_html = pd.DataFrame({"start": ["<span style='color:blue'>"], "end": ["</span>"]}, index=["DEFAULT"])

# r2py:entity:hilight
def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    # Handle vector input (list of strings) like R does
    if isinstance(code, list):
        results = [hilight(c, format_val, markup, prompt, fallback) for c in code]
        return results
    
    if not code:
        return ""

    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html

    # Use Pygments for actual highlighting logic
    lexer = get_lexer_by_name('r')
    formatter = LatexFormatter() if format_val == "latex" else HtmlFormatter()
    
    highlighted = pygments.highlight(code, lexer, formatter)
    
    if prompt:
        # Simple simulation of R prompt adding
        p1 = "> "
        p2 = "+ "
        # In a real scenario, these would be escaped based on format
        return f"{p1}{highlighted}"
    
    return highlighted

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, **kwargs, format_val="latex")

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, **kwargs, format_val="html")

# r2py:entity:hilight
hilight_res = hilight("x=1 # assignment")

# r2py:entity:txt
txt = [
    "a <- 1 # something", 
    "c(y=\"world\", z=\"hello\")", 
    "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", 
    "z@child # S4 slot",
    "'special chars <>#$%&_{}'"
]

# r2py:entity:cat
latex_output = hi_latex(txt)
if isinstance(latex_output, list):
    print("\n".join(latex_output))
else:
    print(latex_output)

# r2py:entity:cat_1
html_output = hi_html(txt)
if isinstance(html_output, list):
    print("\n".join(html_output))
else:
    print(html_output)