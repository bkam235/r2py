# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import re
import html

# Mocking R options
options = {
    "prompt": "> ",
    "continue": "+ "
}

def getOption(opt):
    return options.get(opt, "")

# Highr markup data frames
# In R, highr:::cmd_latex and highr:::cmd_html map token types to wrappers
# r2py:entity:hilight
cmd_latex = pd.DataFrame({
    'start': {
        'def': r'\hldef{', 'kwb': r'\hlkwb{', 'num': r'\hlnum{', 'com': r'\hlcom{',
        'kwd': r'\hlkwd{', 'kwc': r'\hlkwc{', 'kwa': r'\hlkwa{', 'sng': r'\hlsng{',
        'opt': r'\hlopt{', 'DEFAULT': r'\texttt{'
    },
    'end': {
        'def': '}', 'kwb': '}', 'num': '}', 'com': '}',
        'kwd': '}', 'kwc': '}', 'kwa': '}', 'sng': '}',
        'opt': '}', 'DEFAULT': '}'
    }
})

cmd_html = pd.DataFrame({
    'start': {
        'def': '<span class_val="hl def">', 'kwb': '<span class_val="hl kwb">', 'num': '<span class_val="hl num">', 'com': '<span class_val="hl com">',
        'kwd': '<span class_val="hl kwd">', 'kwc': '<span class_val="hl kwc">', 'kwa': '<span class_val="hl kwa">', 'sng': '<span class_val="hl sng">',
        'opt': '<span class_val="hl opt">', 'DEFAULT': '<code>'
    },
    'end': {
        'def': '</span>', 'kwb': '</span>', 'num': '</span>', 'com': '</span>',
        'kwd': '</span>', 'kwc': '</span>', 'kwa': '</span>', 'sng': '</span>',
        'opt': '</span>', 'DEFAULT': '</code>'
    }
})

def escape_latex(text):
    chars = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\~', '^': r'\^'}
    return "".join(chars.get(c, c) for c in text)

def escape_html(text):
    return html.escape(text)

def raw_string(x):
    if isinstance(x, (list, pd.Series)):
        return "\n".join(map(str, x))
    return str(x)

def valid_syntax(code, silent=False):
    return True

def hilight_one(code, format_val, markup, escape_fun):
    if not isinstance(code, str):
        code = str(code)
    
    # Simplified tokenizer mimicking highr's behavior
    tokens = []
    # Order: Comments, Strings, Keywords/Operators, Defaults
    patterns = [
        ('com', r'#.*'),
        ('sng', r'(".*?"|\'.*?\')'),
        ('kwb', r'(<-|=)'),
        ('kwa', r'\b(function|for|if|else|break|next|repeat|while)\b'),
        ('kwd', r'\b(c|print|cat|paste|list|vector)\b'),
        ('kwc', r'\b([a-zA-Z_][a-zA-Z0-9_]*)(?=\s*=)'),
        ('num', r'\b\d+(\.\d+)?\b'),
        ('opt', r'([@:<>])'),
        ('def', r'(\s+|[^\w\s]|[^ \t\n\r\f\v])'),
    ]
    
    combined_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
    
    last_pos = 0
    for match in re.finditer(combined_pattern, code):
        # Handle gap (though patterns above cover almost everything)
        if match.start() > last_pos:
            gap = code[last_pos:match.start()]
            tokens.append(( 'def', gap ))
        
        name = match.lastgroup
        val = match.group(name)
        tokens.append((name, val))
        last_pos = match.end()
        
    if last_pos < len(code):
        tokens.append(('def', code[last_pos:]))

    res = ""
    for token_type, text in tokens:
        # If token is whitespace, don't wrap it in markup (match R's output)
        if token_type == 'def' and text.isspace():
            res += text
            continue
            
        start = markup.loc[token_type, 'start'] if token_type in markup.index else markup.loc['DEFAULT', 'start']
        end = markup.loc[token_type, 'end'] if token_type in markup.index else markup.loc['DEFAULT', 'end']
        
        # Highr only escapes inside specific contexts, but generally we escape the content
        # Note: R's highr doesn't always escape whitespace or special chars in tokens
        escaped = escape_fun(text) if token_type != 'sng' else text.replace('"', '&quot;').replace("'", '&apos;') if format_val == 'html' else escape_latex(text)
        # Correction: strings in latex are wrapped but contents are escaped.
        if format_val == 'latex' and token_type == 'sng':
             escaped = escape_latex(text)
        elif format_val == 'html' and token_type == 'sng':
             escaped = html.escape(text)
        else:
             escaped = escape_fun(text)
             
        res += f"{start}{escaped}{end}"
        
    return res

def hi_naive(code, format_val, markup, escape_fun):
    if isinstance(code, str):
        code = [code]
    res = [escape_fun(line) for line in code]
    return res

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if code is None or (isinstance(code, (list, pd.Series)) and len(code) == 0):
        return raw_string(code)
    
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
    
    escape_fun = escape_latex if format_val == "latex" else escape_html
    
    if not fallback and not valid_syntax(code, silent=False):
        import warnings
        warnings.warn("the syntax of the source code is invalid; the fallback mode is used")
        fallback = True
    
    if not prompt:
        if fallback:
            return raw_string(hi_naive(code, format_val, markup, escape_fun))
        else:
            if isinstance(code, str):
                return hilight_one(code, format_val, markup, escape_fun)
            else:
                return raw_string([hilight_one(line, format_val, markup, escape_fun) for line in code])
    
    p1 = escape_fun(getOption("prompt"))
    p2 = escape_fun(getOption("continue"))
    std = markup.loc['DEFAULT'].tolist()
    if all(pd.notna(std)):
        p1 = f"{std[0]}{p1}{std[1]}"
        p2 = f"{std[0]}{p2}{std[1]}"
    
    code_lines = code if isinstance(code, list) else [code]
    res = []
    for line in code_lines:
        h_line = hilight_one(line, format_val, markup, escape_fun)
        res.append(f"{p1}{h_line}") # Simplified prompt logic for the example
        
    return raw_string(res)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# --- Main Script ---
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

# the markup data frames
print(cmd_latex)
print(cmd_html)