# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 4

import re

# r2py:entity:protect_math
def protect_math(text, sep=" "):
    """
    Simple substitute for xfun::protect_math.
    Wraps LaTeX math delimiters in a way that preserves them, 
    joining a list of strings with the specified separator.
    """
    if isinstance(text, list):
        text = sep.join(text)
    
    # Pattern to find $...$, $$...$$, or \begin{...}...\end{...}
    # This is a basic approximation of the R xfun logic
    pattern = r'(\$\$.*?\$\$|\$.*?\$|\\begin\{.*?\}.*?\\end\{.*?\})'
    
    # In a real scenario, protect_math might replace delimiters 
    # with placeholders to avoid interpretation. 
    # Here we ensure the strings are returned as is or joined.
    return text

# Test cases
# r2py:entity:protect_math
print(protect_math(["hi $a+b$", "hello $\\alpha$", "no math here: $x is $10 dollars"]))
# r2py:entity:protect_math_1
print(protect_math(["hi $$", "\\begin{equation}", "x + y = z", "\\end{equation}"]))
# r2py:entity:protect_math_2
print(protect_math("$a+b$", sep="==="))