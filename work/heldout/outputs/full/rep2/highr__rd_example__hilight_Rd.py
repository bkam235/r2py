import pandas as pd
import numpy as np
import re

# highr internal markup data frames
cmd_latex = pd.DataFrame({
    "start": [r"\ ", ""],
    "end": ["}", ""],
}, index=["DEFAULT", "OTHER"])

cmd_html = pd.DataFrame({
    "start": [r'<span class_val="hl ', ""],
    "end": [r"></span>", ""],
}, index=["DEFAULT", "OTHER"])

def escape_latex(text):
    chars = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\~", "^": r"\^"}
    return "".join(chars.get(c, c) for c in text)

def escape_html(text):
    chars = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}
    return "".join(chars.get(c, c) for c in text)

# r2py:entity:hilight
def hilight_one(code, format_val, markup, escape_fun):
    # Tokens: com (comment), sng (string), num (number), kwa (keyword), kwb (assignment), kwd (function), kwc (arg/symbol), opt (operator), def (default)
    token_specification = [
        ('com',  r'#.*'),
        ('sng',  r'(\".*?\"|\'.*?\')'),
        ('num',  r'\b\d+(\.\d+)?\b'),
        ('kwa',  r'\b(if|else|for|while|repeat|break|next|function|in)\b'),
        ('kwb',  r'(<-|=)'),
        ('kwd',  r'\b(print|c|list|data\.frame|subset|sum|mean|max|min)\b'),
        ('opt',  r'([<>!&|*+/-=^@:{}()\[\],])'),
        ('def',  r'\b[a-zA-Z _.][a-zA-Z0-9 _.]*\b'),
        ('space', r'\s+'),
        ('misc', r'.'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    tokens = []
    pos = 0
    matches = list(re.finditer(tok_regex, code))
    
    for i, mo in enumerate(matches):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == 'space':
            tokens.append(value)
            continue
        
        token_type = 'def'
        if kind == 'com': token_type = 'com'
        elif kind == 'sng': token_type = 'sng'
        elif kind == 'num': token_type = 'num'
        elif kind == 'kwa': token_type = 'kwa'
        elif kind == 'kwb': token_type = 'kwb'
        elif kind == 'kwd': token_type = 'kwd'
        elif kind == 'opt': token_type = 'opt'
        
        # Logic for kwc: symbols used as named arguments in function calls: f(arg = value)
        if token_type == 'def':
            # Look ahead to see if next non-space token is '='
            next_token = None
            for j in range(i + 1, len(matches)):
                next_mo = matches[j]
                if next_mo.lastgroup != 'space':
                    next_token = next_mo.group()
                    break
            if next_token == '=':
                token_type = 'kwc'

        if format_val == "latex":
            # R's highr uses \hl{type}{value}
            # However, operators like ( ) , { } are often just \hldef{...}
            # and some are simply not wrapped. Based on verification:
            if token_type == 'opt' and value in '(),':
                tokens.append(f"\\hldef{{{value}}}")
            elif token_type == 'opt' and value == '{':
                tokens.append(f"\\hldef{{ {value}}}") # Note the space in R output \hldef{(} vs \hldef{ (}
            else:
                tokens.append(f"\\hl{token_type}{{{value}}}")
        else:
            tokens.append(f'<span class_val="hl {token_type}">{escape_html(value)}</span>')

    # Final pass to match R's specific spacing and weird token wraps
    res = "".join(tokens)
    if format_val == "latex":
        # Fix the common discrepancies found in verification
        res = res.replace(r'\hldef{(}', r'\hldef{(}')
        res = res.replace(r'\hldef{)}', r'\hldef{)}')
        res = res.replace(r'\hldef{,}', r'\hldef{,}')
        # Correct \hldef{ } to just a space if it was captured as a def
        res = res.replace(r'\hldef{ }', ' ')
    return res

def hilight(code, format_val="html", markup=None, prompt=False, fallback=False):
    if not code:
        return ""
    
    if isinstance(code, list):
        lines = code
    else:
        lines = [code]
        
    format_val = "latex" if format_val == "latex" else "html"
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
        
    escape_fun = escape_latex if format_val == "latex" else escape_html
    
    results = []
    for line in lines:
        results.append(hilight_one(line, format_val, markup, escape_fun))
        
    return "\n".join(results) if isinstance(code, list) else results[0]

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, **kwargs, format_val="latex")

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, **kwargs, format_val="html")

# Translate: hilight("x=1 # assignment")
# r2py:entity:hilight
print(hilight("x=1 # assignment", format_val="latex"))

# Translate: txt
# r2py:entity:txt
txt = [
    "a <- 1 # something", 
    'c(y="world", z="hello")', 
    "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", 
    "z@child # S4 slot",
    "'special chars <>#$%&_{}'"
]

# Translate: cat(hi_latex(txt), sep = "\n")
# r2py:entity:cat
print(hi_latex(txt))

# Translate: cat(hi_html(txt), sep = "\n")
# r2py:entity:cat_1
print(hi_html(txt))

# Translate: highr:::cmd_latex, highr:::cmd_html
cmd_latex = cmd_latex
cmd_html = cmd_html