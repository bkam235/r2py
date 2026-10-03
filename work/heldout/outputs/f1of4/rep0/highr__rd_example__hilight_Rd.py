import pandas as pd
import numpy as np
import re

# Mocking highr internal data frames
cmd_latex = pd.DataFrame({
    "start": ["\\hl", "\\hl", "\\hl", "\\hl", "\\hl", "\\hl", ""],
    "end": ["def}", "kwb}", "num}", "com}", "kwd}", "sng}", ""],
}, index=["def", "kwb", "num", "com", "kwd", "sng", "DEFAULT"])

cmd_html = pd.DataFrame({
    "start": ["<span class_val=\"hl def\">", "<span class_val=\"hl kwb\">", "<span class_val=\"hl num\">", 
              "<span class_val=\"hl com\">", "<span class_val=\"hl kwd\">", "<span class_val=\"hl sng\">", ""],
    "end": ["</span>", "</span>", "</span>", "</span>", "</span>", "</span>", ""],
}, index=["def", "kwb", "num", "com", "kwd", "sng", "DEFAULT"])

def escape_latex(text):
    return text.replace("_", "\\_").replace("{", "\\{").replace("}", "\\}")

def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# r2py:entity:hilight
def hilight_one(code, format_val, markup, escape_fun):
    if not code:
        return ""
    
    # Define token patterns in order of priority
    # R Lexer approximation
    tokens = [
        ('com', r'#.*'),
        ('sng', r'\'(.*?)\'|"(.*?)"'),
        ('kwa', r'\b(function|for|if|else|break|in)\b'),
        ('kwb', r'(<-|=)'),
        ('num', r'\b\d+(\.\d+)?\b'),
        ('kwd', r'\b(c|print)\b'),
        ('kwc', r'\b[a-zA-Z_][a-zA-Z0-9_.]*\b(?=\s*=)'),
        ('opt', r'[:@<>]'),
        ('def', r'\b[a-zA-Z_][a-zA-Z0-9_.]*\b'),
        ('other', r'.'),
    ]
    
    pattern = '|'.join(f'(?P<{name}>{regex})' for name, regex in tokens)
    
    result = []
    for match in re.finditer(pattern, code):
        kind = match.lastgroup
        value = match.group(kind)
        
        if kind == 'other':
            result.append(escape_fun(value))
            continue
            
        if format_val == "latex":
            # highr uses \hl{type}{value} syntax
            # Mapping internal token names to highr's latex tags
            tag_map = {'com': 'com', 'sng': 'sng', 'kwa': 'kwa', 'kwb': 'kwb', 
                       'num': 'num', 'kwd': 'kwd', 'kwc': 'kwc', 'opt': 'opt', 'def': 'def'}
            tag = tag_map.get(kind, 'def')
            result.append(f"\\hl{tag}{{{escape_fun(value)}}}")
        else:
            # HTML format
            tag_map = {'com': 'com', 'sng': 'sng', 'kwa': 'kwa', 'kwb': 'kwb', 
                       'num': 'num', 'kwd': 'kwd', 'kwc': 'kwc', 'opt': 'opt', 'def': 'def'}
            tag = tag_map.get(kind, 'def')
            result.append(f'<span class_val="hl {tag}">{escape_fun(value)}</span>')
            
    return "".join(result)

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if code is None or (isinstance(code, (list, np.ndarray)) and len(code) == 0):
        return ""
    
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
    
    escape_fun = escape_latex if format_val == "latex" else escape_html
    
    if not prompt:
        if isinstance(code, (list, np.ndarray)):
            return [hilight_one(line, format_val, markup, escape_fun) for line in code]
        else:
            return hilight_one(code, format_val, markup, escape_fun)
    
    # Prompt logic implementation
    # Use defaults from R options if not provided
    p1 = escape_fun("> ") 
    p2 = escape_fun("+ ")
    
    std_start = markup.loc["DEFAULT", "start"]
    std_end = markup.loc["DEFAULT", "end"]
    
    p1 = f"{std_start}{p1}{std_end}"
    p2 = f"{std_start}{p2}{std_end}"
    
    if isinstance(code, str):
        code = [code]
        
    lines = []
    for block in code:
        # split_source approximation: split by newline but keep structure
        sublines = block.split('\n')
        highlighted_sublines = [hilight_one(sl, format_val, markup, escape_fun) for sl in sublines]
        
        # Prepend prompts
        prompted = [p1 + highlighted_sublines[0]]
        for sl in highlighted_sublines[1:]:
            prompted.append(p2 + sl)
        lines.append("\n".join(prompted))
        
    return "\n".join(lines)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, **kwargs, format_val="latex")

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, **kwargs, format_val="html")

# Execution
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
res_latex = hi_latex(txt)
if isinstance(res_latex, list):
    print("\n".join(res_latex))
else:
    print(res_latex)

# r2py:entity:cat_1
res_html = hi_html(txt)
if isinstance(res_html, list):
    print("\n".join(res_html))
else:
    print(res_html)

# Access internal data frames
cmd_latex = cmd_latex
cmd_html = cmd_html