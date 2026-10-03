import pandas as pd
import re
import html

# Mocking the highr internal markup data frames
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
}, index=['def', 'kwb', 'num', 'com', 'kwd', 'kwc', 'kwa', 'sng', 'opt', 'DEFAULT'])

cmd_html = pd.DataFrame({
    'start': {
        'def': '<span class="hl def">', 'kwb': '<span class="hl kwb">', 'num': '<span class="hl num">', 'com': '<span class="hl com">',
        'kwd': '<span class="hl kwd">', 'kwc': '<span class="hl kwc">', 'kwa': '<span class="hl kwa">', 'sng': '<span class="hl sng">',
        'opt': '<span class="hl opt">', 'DEFAULT': '<code>'
    },
    'end': {
        'def': '</span>', 'kwb': '</span>', 'num': '</span>', 'com': '</span>',
        'kwd': '</span>', 'kwc': '</span>', 'kwa': '</span>', 'sng': '</span>',
        'opt': '</span>', 'DEFAULT': '</code>'
    }
}, index=['def', 'kwb', 'num', 'com', 'kwd', 'kwc', 'kwa', 'sng', 'opt', 'DEFAULT'])

def escape_latex(text):
    chars = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
        '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\~',
        '^': r'\^', '\\': r'\textbackslash{}'
    }
    return "".join(chars.get(c, c) for c in text)

def escape_html(text):
    return html.escape(text)

def raw_string(x):
    if isinstance(x, (list, pd.Series)):
        return "\n".join(map(str, x))
    return str(x)

def valid_syntax(code, silent=False):
    return True

def hi_naive(code, format_val, markup, escape_fun):
    if isinstance(code, list):
        return [escape_fun(line) for line in code]
    return escape_fun(code)

def hilight_one(code, format_val, markup, escape_fun):
    if isinstance(code, list):
        return [hilight_one(line, format_val, markup, escape_fun) for line in code]
    
    # Pattern to match R tokens
    # Groups: 1:Comment, 2:String, 3:Assign, 4:Keyword, 5:Number, 6:Identifier, 7:Punctuation
    pattern = r'(#.*)|(".*?"|\'.*?\')|(<-|=)|(\bfunction\b|\bfor\b|\bif\b|\belse\b|\bbreak\b|\bin\b)|(\b\d+\b)|(\b[a-zA-Z_][a-zA-Z0-9_.]*\b)|([@<>\(\),;:])'
    
    tokens = []
    last_end = 0
    
    for match in re.finditer(pattern, code):
        start, end = match.span()
        if start > last_end:
            txt = code[last_end:start]
            # R's highr generally does NOT wrap whitespace in DEFAULT tags
            if txt.strip() == "":
                tokens.append(txt)
            else:
                tokens.append(f"{markup.loc['DEFAULT', 'start']}{escape_fun(txt)}{markup.loc['DEFAULT', 'end']}")
        
        val = match.group(0)
        if match.group(1): # Comment
            tag = 'com'
        elif match.group(2): # String
            tag = 'sng'
        elif match.group(3): # Assignment
            tag = 'kwb'
        elif match.group(4): # Keyword
            tag = 'kwa'
        elif match.group(5): # Number
            tag = 'num'
        elif match.group(6): # Identifier
            if val in ('c', 'print'):
                tag = 'kwd'
            else:
                tag = 'def'
        elif match.group(7): # Punctuation
            if val in ('(', ')', ','):
                tag = 'def'
            else:
                tag = 'opt'
        else:
            tag = 'def'

        tokens.append(f"{markup.loc[tag, 'start']}{escape_fun(val)}{markup.loc[tag, 'end']}")
        last_end = end
    
    if last_end < len(code):
        txt = code[last_end:]
        if txt.strip() == "":
            tokens.append(txt)
        else:
            tokens.append(f"{markup.loc['DEFAULT', 'start']}{escape_fun(txt)}{markup.loc['DEFAULT', 'end']}")

    result = "".join(tokens)
    
    # Post-process for keyword arguments: identifier before '=' becomes kwc, '=' becomes def
    if format_val == "latex":
        result = re.sub(r'\\hl(?:def|kwd)\{([a-zA-Z_][a-zA-Z0-9_.]*)\}\\hlkwb{=}', r'\\hlkwc{\1}\\hldef{=}', result)
    else:
        result = re.sub(r'<span class="hl (?:def|kwd)">([a-zA-Z_][a-zA-Z0-9_.]*)</span><span class="hl kwb">=</span>', 
                        r'<span class="hl kwc">\1</span><span class="hl def">=</span>', result)

    return result

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
        res = func(code, format_val, markup, escape_fun)
        return raw_string(res)
    
    p1 = escape_fun("> ")
    p2 = escape_fun("+ ")
    std = markup.loc["DEFAULT"].values
    if not any(pd.isna(std)):
        p1 = f"{std[0]}{p1}{std[1]}"
        p2 = f"{std[0]}{p2}{std[1]}"
        
    code_lines = code.split('\n') if isinstance(code, str) else code
    res = [hilight_one(line, format_val, markup, escape_fun) for line in code_lines]
    
    final_output = []
    for i, line in enumerate(res):
        prefix = p1 if i == 0 else p2
        final_output.append(f"{prefix}{line}")
        
    return raw_string(final_output)

def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# Main script execution
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

print(cmd_latex)
print(cmd_html)