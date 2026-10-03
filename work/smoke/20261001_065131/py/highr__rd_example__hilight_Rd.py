# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import re

# Mocking highr internal data frames as the actual logic relies on these lookup tables
# These are simplified representations of cmd_latex and cmd_html
cmd_latex = pd.DataFrame({
    'start': ['\\texttt{', '\\texttt{'],
    'end': ['}', '}']
}, index=['DEFAULT', 'KEYWORD'])

cmd_html = pd.DataFrame({
    'start': ['<span class="default">', '<span class="keyword">'],
    'end': ['</span>', '</span>']
}, index=['DEFAULT', 'KEYWORD'])

def escape_latex(text):
    chars = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}'}
    return "".join(chars.get(c, c) for c in text)

def escape_html(text):
    chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return "".join(chars.get(c, c) for c in text)

def raw_string(x):
    if isinstance(x, list):
        return "\n".join(x)
    return str(x)

def valid_syntax(code, silent=False):
    # Simplification: assume syntax is valid for this translation
    return True

def hi_naive(code, format_val, markup, escape_fun):
    # Fallback mode: just escape and wrap in default markup
    std_start = markup.loc['DEFAULT', 'start'] if 'DEFAULT' in markup.index else ""
    std_end = markup.loc['DEFAULT', 'end'] if 'DEFAULT' in markup.index else ""
    if isinstance(code, list):
        return [f"{std_start}{escape_fun(line)}{std_end}" for line in code]
    return f"{std_start}{escape_fun(code)}{std_end}"

def hilight_one(code, format_val, markup, escape_fun):
    # Basic implementation of syntax highlighting logic
    # In a real scenario, this would use a tokenizer
    if isinstance(code, list):
        return [hilight_one(line, format_val, markup, escape_fun) for line in code]
    
    # Simple regex to simulate highlighting (e.g., comments)
    res = code
    if "#" in res:
        parts = res.split("#", 1)
        # Comment part is typically highlighted differently in highr
        res = f"{escape_fun(parts[0])}# {escape_fun(parts[1])}"
    else:
        res = escape_fun(res)
        
    std_start = markup.loc['DEFAULT', 'start'] if 'DEFAULT' in markup.index else ""
    std_end = markup.loc['DEFAULT', 'end'] if 'DEFAULT' in markup.index else ""
    return f"{std_start}{res}{std_end}"

# r2py:entity:hilight
def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if not code or (isinstance(code, list) and len(code) == 0):
        return raw_string(code)
    
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
    
    escape_fun = escape_latex if format_val == "latex" else escape_html
    
    if not fallback and not valid_syntax(code, silent=False):
        import warnings
        warnings.warn("the syntax of the source code is invalid; the fallback mode is used")
        fallback = True
        
    if not prompt:
        func = hi_naive if fallback else hilight_one
        return raw_string(func(code, format_val, markup, escape_fun))
    
    # Prompt logic (simplified)
    p1 = escape_fun("> ")
    p2 = escape_fun("+ ")
    
    if isinstance(code, str):
        code = [code]
    
    res = []
    for line in code:
        highlighted = hilight_one(line, format_val, markup, escape_fun)
        res.append(f"{p1}{highlighted}")
        
    return raw_string(res)

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
print(hi_latex(txt))
# r2py:entity:cat_1
print(hi_html(txt))

# The markup data frames
print(cmd_latex)
print(cmd_html)