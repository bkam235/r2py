# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# r2py:entity:cat
def highlight(code):
    # downlit provides syntax highlighting for R code. 
    # In Python, pygments is the standard for this.
    # Using PythonLexer as a proxy for the highlighting logic.
    formatter = HtmlFormatter()
    return pygments.highlight(code, PythonLexer(), formatter)

# r2py:entity:cat
print(highlight("1 + 1"))
# r2py:entity:cat_1
print(highlight("base::t(1:3)"))
# r2py:entity:cat_2
print(highlight("base::t("))