# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
import re
import html

# Mocking the internal highr markup data frames as they are required by the logic
# cmd_latex and cmd_html usually map token types to LaTeX/HTML commands
cmd_latex = pd.DataFrame({
    'start': ['\\texttt{', '\\textbf{', '\\textcolor{blue}{'],
    'end': ['}', '}', '}']
}, index=['KEYWORD', 'STRING', 'COMMENT'])
# Adding the DEFAULT row referenced in the source
cmd_latex.loc['DEFAULT'] = ['\\texttt{', '}']

cmd_html = pd.DataFrame({
    'start': ['<span class_val="keyword">', '<span class_val="string">', '<span class_val="comment">'],
    'end': ['</span>', '</span>', '</span>']
}, index=['KEYWORD', 'STRING', 'COMMENT'])
cmd_html.loc['DEFAULT'] = ['<code>', '</code>']

def escape_latex(text):
    replacements = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}'}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def escape_html(text):
    return html.escape(text)

# r2py:entity:hilight
def valid_syntax(code, silent=False):
    # Highr checks R syntax; for Python translation we approximate as True 
    # since the input strings provided are R code strings.
    return True

def raw_string(res):
    if isinstance(res, (list, np.ndarray)):
        return "\n".join(res)
    return str(res)

def hi_naive(code, format_val, markup, escape_fun):
    # Fallback highlighter: just wraps the whole thing in DEFAULT markup
    std = markup.loc['DEFAULT'].tolist()
    if isinstance(code, list):
        return [f"{std[0]}{escape_fun(line)}{std[1]}" for line in code]
    return f"{std[0]}{escape_fun(code)}{std[1]}"

def hilight_one(code, format_val, markup, escape_fun):
    # Simplified highlighting logic simulating highr's tokenization
    # In a real scenario, this would use a lexer.
    if isinstance(code, list):
        return [hilight_one(line, format_val, markup, escape_fun) for line in code]
    
    # Dummy logic: highlight comments (#) and strings ("")
    res = escape_fun(code)
    if '#' in res:
        parts = res.split('#', 1)
        comment_markup = markup.loc['COMMENT'] if 'COMMENT' in markup.index else markup.loc['DEFAULT']
        res = f"{parts[0]}{comment_markup[0]}# {parts[1]}{comment_markup[1]}"
    return res

def split_source(code):
    if isinstance(code, str):
        return [code]
    return code

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if code is None or (isinstance(code, (list, np.ndarray)) and len(code) == 0):
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
    
    # Prompt logic
    p1 = escape_fun("> ") # Default R prompt
    p2 = escape_fun("+ ") # Default R continue
    
    std = markup.loc['DEFAULT'].tolist()
    if len(std) >= 2 and not any(pd.isna(std)):
        p1 = f"{std[0]}{p1}{std[1]}"
        p2 = f"{std[0]}{p2}{std[1]}"
    
    code_split = split_source(code)
    res = []
    for block in code_split:
        highlighted_lines = hilight_one(block, format_val, markup, escape_fun)
        if isinstance(highlighted_lines, list):
            lines = [f"{p1 if i == 0 else p2}{line}" for i, line in enumerate(highlighted_lines)]
            res.append("\n".join(lines))
        else:
            res.append(f"{p1}{highlighted_lines}")
            
    return raw_string(res)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# --- Execution ---
# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# r2py:entity:txt
txt = ["a <- 1 # something", "c(y=\"world\", z=\"hello\")", "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", "z@child # S4 slot",
    "'special chars <>#$%&_{}'"]

# r2py:entity:cat
print(hi_latex(txt))
# r2py:entity:cat_1
print(hi_html(txt))

# The markup data frames
print(cmd_latex)
print(cmd_html)