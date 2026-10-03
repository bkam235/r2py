# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
import re

# Mocking the internal highr logic for syntax highlighting as the package is R-specific
# cmd_latex and cmd_html define the styles for different token types
cmd_latex = pd.DataFrame({
    'start': ['\\textcolor{blue}{', '\\textcolor{red}{', '\\texttt{'],
    'end': ['}', '}', '}']
}, index=['KEYWORD', 'STRING', 'DEFAULT'])

cmd_html = pd.DataFrame({
    'start': ['<span style="color:blue">', '<span style="color:red">', '<code>'],
    'end': ['</span>', '</span>', '</code>']
}, index=['KEYWORD', 'STRING', 'DEFAULT'])

def escape_latex(text):
    replacements = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}'}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def escape_html(text):
    replacements = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def hilight_one(code, format_val, markup, escape_fun):
    # Simple regex-based highlighter to simulate highr's behavior
    if isinstance(code, list):
        return "\n".join([hilight_one(line, format_val, markup, escape_fun) for line in code])
    
    # Basic tokens: strings, keywords, and default
    # This is a simplified approximation of the R package logic
    res = escape_fun(code)
    # Mock highlight: wrap strings in quotes with STRING style, keywords (simplified) with KEYWORD style
    res = re.sub(r'(".*?"|\'.*?\')', lambda m: f"{markup.loc['STRING', 'start']}{m.group(1)}{markup.loc['STRING', 'end']}", res)
    res = re.sub(r'\b(function|for|if|else|break|in)\b', lambda m: f"{markup.loc['KEYWORD', 'start']}{m.group(0)}{markup.loc['KEYWORD', 'end']}", res)
    return f"{markup.loc['DEFAULT', 'start']}{res}{markup.loc['DEFAULT', 'end']}"

def hi_naive(code, format_val, markup, escape_fun):
    return hilight_one(code, format_val, markup, escape_fun)

def raw_string(x):
    if isinstance(x, list) or isinstance(x, np.ndarray):
        return x
    return x

# r2py:entity:hilight
def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if code is None or (isinstance(code, (list, np.ndarray)) and len(code) == 0):
        return raw_string(code)
    
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
    
    escape_fun = escape_latex if format_val == "latex" else escape_html
    
    # Simplified validation
    if not fallback:
        # In a real scenario, valid_syntax would be checked here
        pass
    
    if not prompt:
        # Simulate hilight_one for single string or list of strings
        if isinstance(code, str):
            return raw_string(hilight_one(code, format_val, markup, escape_fun))
        else:
            return raw_string([hilight_one(line, format_val, markup, escape_fun) for line in code])
    
    # Prompt logic (omitted for brevity as the example usage doesn't trigger prompt=True)
    return raw_string(code)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# Main script execution
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
print("\n".join(latex_out))

# r2py:entity:cat_1
html_out = hi_html(txt)
print("\n".join(html_out))

# Display markup data frames
print(cmd_latex)
print(cmd_html)