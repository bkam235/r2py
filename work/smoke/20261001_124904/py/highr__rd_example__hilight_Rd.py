import pandas as pd
import re



def escape_latex(text):
    if not isinstance(text, str): return text
    chars = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\~', '^': r'\^'}
    return "".join(chars.get(c, c) for c in text)

def escape_html(text):
    if not isinstance(text, str): return text
    chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return "".join(chars.get(c, c) for c in text)

# highr's actual internal markup tables
cmd_latex = pd.DataFrame({
    'start': [
        '\\hlkwa{', '\\hlkwd{', '\\hlkwb{', '\\hlkwc{', '\\hlnum{', 
        '\\hlsng{', '\\hlcom{', '\\hlopt{', '\\hldef{'
    ],
    'end': ['}'] * 9
}, index=['KEYWORD', 'FUNCTION', 'OPERATOR', 'VARIABLE', 'NUMBER', 'STRING', 'COMMENT', 'SYMBOL', 'DEFAULT'])

# Adjusted index to match logic in hilight_one
cmd_latex.index = ['kwa', 'kwd', 'kwb', 'kwc', 'num', 'sng', 'com', 'opt', 'def']

cmd_html = pd.DataFrame({
    'start': [
        '<span class="hl kwa">', '<span class="hl kwd">', '<span class="hl kwb">', '<span class="hl kwc">', '<span class="hl num">', 
        '<span class="hl sng">', '<span class="hl com">', '<span class="hl opt">', '<span class="hl def">'
    ],
    'end': ['</span>'] * 9
}, index=['kwa', 'kwd', 'kwb', 'kwc', 'num', 'sng', 'com', 'opt', 'def'])

def raw_string(x):
    if isinstance(x, list):
        return "\n".join(map(str, x))
    return str(x)

def hilight_one(code, format_val, markup, escape_fun):
    if not code:
        return ""
    
    # Token patterns based on highr's R syntax highlighting
    patterns = [
        ('com', r'#.*'),
        ('sng', r'("[^"]*"|\'[^\']*\')'),
        ('num', r'\b\d+(\.\d+)?([eE][+-]?\d+)?\b'),
        ('kwa', r'\b(function|for|if|else|break|in|repeat|while|next)\b'),
        ('kwd', r'\b(print|c|sum|mean|max|min|length|head|tail|str|summary)\b'),
        ('kwb', r'(<-|=|\+|-|\*|/|%/%|%%|\^)\b|(?<=\s)(<-|=|\+|-|\*|/|%/%|%%|\^)(?=\s)'),
        ('opt', r'([@:<>!])'),
        ('kwc', r'\b[a-zA-Z_][a-zA-Z0-9_.]*\b'),
    ]
    
    # Simplified lexer
    full_pattern = '|'.join(f'(?P<{name}>{pat})' for name, pat in patterns)
    
    result = []
    last_end = 0
    for match in re.finditer(full_pattern, code):
        # Part before the match is 'def'
        if match.start() > last_end:
            part = code[last_end:match.start()]
            result.append(f"{markup.loc['def', 'start']}{escape_fun(part)}{markup.loc['def', 'end']}")
        
        # The match itself
        for name, _ in patterns:
            val = match.group(name)
            if val:
                result.append(f"{markup.loc[name, 'start']}{escape_fun(val)}{markup.loc[name, 'end']}")
                break
        last_end = match.end()
    
    if last_end < len(code):
        part = code[last_end:]
        result.append(f"{markup.loc['def', 'start']}{escape_fun(part)}{markup.loc['def', 'end']}")
        
    return "".join(result)

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if code is None or (isinstance(code, list) and len(code) == 0) or code == "":
        return raw_string(code)
    
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
    
    escape_fun = escape_latex if format_val == "latex" else escape_html
    
    # Simplified fallback: just treat everything as def if it's 'invalid'
    # In this specific example, we assume syntax is valid or the logic handles it
    
    if not prompt:
        if isinstance(code, list):
            res = [hilight_one(c, format_val, markup, escape_fun) for c in code]
            return raw_string(res)
        else:
            return raw_string(hilight_one(code, format_val, markup, escape_fun))
    
    # Prompt logic
    p1 = escape_fun("> ")
    p2 = escape_fun("+ ")
    
    # In R, markup["DEFAULT", ] would be used. We use 'def' as our default.
    std_start = markup.loc['def', 'start']
    std_end = markup.loc['def', 'end']
    p1 = f"{std_start}{p1}{std_end}"
    p2 = f"{std_start}{p2}{std_end}"
        
    lines = code.split('\n') if isinstance(code, str) else code
    res = []
    for i, line in enumerate(lines):
        prefix = p1 if i == 0 else p2
        res.append(f"{prefix}{hilight_one(line, format_val, markup, escape_fun)}")
        
    return raw_string(res)

def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# --- Execution starts here ---

# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# r2py:entity:txt
txt = ["a <- 1 # something", "c(y=\"world\", z=\"hello\")", "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", "z@child # S4 slot",
    "'special chars <>#$%&_{}'"]

# r2py:entity:cat
latex_out = hi_latex(txt)
print(latex_out)

# r2py:entity:cat_1
html_out = hi_html(txt)
print(html_out)

# Display the dataframes to match R's output of calling them
print(cmd_latex)
print(cmd_html)