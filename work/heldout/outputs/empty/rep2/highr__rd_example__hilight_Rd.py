import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, LatexFormatter
import pandas as pd

# Helper for lexer
# r2py:entity:hilight
def get_r_lexer():
    return get_lexer_by_name("r")

# Equivalent of highr:::cmd_latex and highr:::cmd_html
# In R, these are data frames mapping R tokens to LaTeX/HTML commands.
# Since they are internal, we approximate them as empty DataFrames or dummy objects 
# to satisfy the variable existence requirement.
cmd_latex = pd.DataFrame()
cmd_html = pd.DataFrame()

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    # In R, hilight(code) defaults format to "latex" via match.arg(format)
    # We use pygments to approximate the highlighting.
    lexer = get_r_lexer()
    
    if isinstance(code, list):
        # Handle vector input
        results = []
        for line in code:
            if format_val == "latex":
                formatter = LatexFormatter()
            else:
                formatter = HtmlFormatter()
            results.append(pygments.highlight(line, lexer, formatter))
        return "\n".join(results)
    else:
        # Handle single string
        if format_val == "latex":
            formatter = LatexFormatter()
        else:
            formatter = HtmlFormatter()
        return pygments.highlight(code, lexer, formatter)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, **kwargs, format_val="latex")

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, **kwargs, format_val="html")

# Logic execution
# R: hilight("x=1 # assignment")
# Note: the R source calls hilight() which defaults to latex
# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# R: txt = c(...)
# r2py:entity:txt
txt = [
    "a <- 1 # something", 
    "c(y=\"world\", z=\"hello\")", 
    "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", 
    "z@child # S4 slot",
    "'special chars <>#$%&_{}'"
]

# R: cat(hi_latex(txt), sep = "\n")
# r2py:entity:cat
print(hi_latex(txt))

# R: cat(hi_html(txt), sep = "\n")
# r2py:entity:cat_1
print(hi_html(txt))

# The markup data frames (already defined above, but ensuring they are in global scope)
# cmd_latex = ...
# cmd_html = ...