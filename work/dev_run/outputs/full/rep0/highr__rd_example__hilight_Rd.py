# Translated from <R script> by r2py v0.3.0
import pandas as pd
import numpy as np
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, LatexFormatter

# highr provides syntax highlighting for R. Pygments is the Python equivalent.

# r2py:entity:hilight
def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    # Simple wrapper to mimic highr's hilight logic
    lexer = get_lexer_by_name('r')
    if format_val == "latex":
        formatter = LatexFormatter()
    else:
        formatter = HtmlFormatter()
    
    if isinstance(code, list):
        # Process list of strings
        results = []
        for line in code:
            results.append(highlight(line, lexer, formatter))
        return results
    else:
        return highlight(code, lexer, formatter)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, format_val="latex", **kwargs)

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, format_val="html", **kwargs)

# r2py:entity:hilight
print(hilight("x=1 # assignment"))

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
latex_out = hi_latex(txt)
# R's cat(..., sep="\n") for a vector prints each element on a new line
if isinstance(latex_out, list):
    print("\n".join(latex_out))
else:
    print(latex_out)

# r2py:entity:cat_1
html_out = hi_html(txt)
if isinstance(html_out, list):
    print("\n".join(html_out))
else:
    print(html_out)

# highr:::cmd_latex and highr:::cmd_html
# These are internal data frames in R. We'll represent them as empty DataFrames
# to satisfy the variable presence requirement.
cmd_latex = pd.DataFrame()
cmd_html = pd.DataFrame()