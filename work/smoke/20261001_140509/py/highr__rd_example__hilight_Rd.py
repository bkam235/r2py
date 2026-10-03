import pandas as pd
import re
import html

# r2py:entity:cat
def escape_latex(text):
    chars = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\~', '^': r'\^',
        '\\': r'\\', '<': r'\textless', '>': r'\textgreater'
    }
    return "".join(chars.get(c, c) for c in text)

# r2py:entity:cat_1
def escape_html(text):
    return html.escape(text)

# highr's internal markup tables
cmd_latex = pd.DataFrame({
    'start': [
        '\\hldef{', '\\hlkwa{', '\\hlkwb{', '\\hlkwc{', '\\hlkwd{', 
        '\\hlnum{', '\\hlopt{', '\\hlsng{', '\\hlcom{'
    ],
    'end': ['}', '}', '}', '}', '}', '}', '}', '}', '}'],
}, index=['def', 'kwa', 'kwb', 'kwc', 'kwd', 'num', 'opt', 'sng', 'com'])

cmd_latex.loc['DEFAULT'] = pd.Series({'start': '\\hldef{', 'end': '}'})

cmd_html = pd.DataFrame({
    'start': [
        '<span class="hl def">', '<span class="hl kwa">', '<span class="hl kwb">', 
        '<span class="hl kwc">', '<span class="hl kwd">', '<span class="hl num">', 
        '<span class="hl opt">', '<span class="hl sng">', '<span class="hl com">'
    ],
    'end': ['</span>'] * 9,
}, index=['def', 'kwa', 'kwb', 'kwc', 'kwd', 'num', 'opt', 'sng', 'com'])

cmd_html.loc['DEFAULT'] = pd.Series({'start': '<span class="hl def">', 'end': '</span>'})

# r2py:entity:hilight
def raw_string(code):
    if isinstance(code, list):
        return "\n".join(code)
    return code

def valid_syntax(code, silent=False):
    return True

def split_source(code):
    if isinstance(code, str):
        return [code]
    return code

def hi_naive(code, format_val, markup, escape_fun):
    return f"{markup.loc['DEFAULT', 'start']}{code}{markup.loc['DEFAULT', 'end']}"

def hilight_one(code, format_val, markup, escape_fun):
    if isinstance(code, list):
        code = "\n".join(code)
    
    # Refined patterns to match highr's behavior:
    # R's highr treats many things (identifiers, punctuation) as 'def'
    patterns = [
        ('com', r'#.*'),
        ('sng', r'".*?"|\'.*?\''),
        ('num', r'\b\d+(\.\d+)?\b'),
        ('kwa', r'\b(function|for|if|else|break|in|repeat|while|next)\b'),
        ('kwb', r'<-|='),
        ('kwd', r'\b(print|c|cat|paste|paste0|list|seq|rep)\b'),
        ('opt', r'[@:<>!\+*/\-%]'),
        # All other non-whitespace characters fall into 'def'
        ('def', r'\S'), 
    ]
    
    master_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns))
    
    result = []
    last_pos = 0
    for match in master_re.finditer(code):
        if match.start() > last_pos:
            gap = code[last_pos:match.start()]
            result.append(gap)
            
        for name, value in match.groupdict().items():
            if value is not None:
                key = name if name in markup.index else 'DEFAULT'
                result.append(f"{markup.loc[key, 'start']}{value}{markup.loc[key, 'end']}")
                break
        last_pos = match.end()
    
    if last_pos < len(code):
        result.append(code[last_pos:])
        
    return "".join(result)

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if code is None or (isinstance(code, list) and len(code) == 0):
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
    
    p1 = escape_fun("> ")
    p2 = escape_fun("+ ")
    std = markup.loc['DEFAULT']
    p1 = f"{std['start']}{p1}{std['end']}"
    p2 = f"{std['start']}{p2}{std['end']}"
    
    code_split = split_source(code)
    res = []
    for segment in code_split:
        highlighted = hilight_one(segment, format_val, markup, escape_fun)
        lines = highlighted.split('\n')
        formatted_lines = [f"{p1}{lines[0]}"]
        for line in lines[1:]:
            formatted_lines.append(f"{p2}{line}")
        res.append("\n".join(formatted_lines))
    
    return raw_string(res)

def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# Execution
# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# r2py:entity:txt
txt = ["a <- 1 # something", "c(y=\"world\", z=\"hello\")", "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", "z@child # S4 slot",
    "'special chars <>#$%&_{}'"]

# r2py:entity:cat
print("\n".join([hi_latex(line) for line in txt]))
# r2py:entity:cat_1
print("\n".join([hi_html(line) for line in txt]))

print(cmd_latex)
print(cmd_html)