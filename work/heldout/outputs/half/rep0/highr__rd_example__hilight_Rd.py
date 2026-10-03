import pandas as pd
import numpy as np
import re
import html

# r2py:entity:hilight
cmd_latex = pd.DataFrame({
    "start": ["\\hldef{", "\\hlkwb{", "\\hlnum{", "\\hlcom{", "\\hlkwd{", "\\hlkwc{", "\\hlkwa{", "\\hlopt{", "\\hlsng{"],
    "end": ["}", "}", "}", "}", "}", "}", "}", "}", "}"],
    "token": ["def", "kwb", "num", "com", "kwd", "kwc", "kwa", "opt", "sng"]
}, index=["def", "kwb", "num", "com", "kwd", "kwc", "kwa", "opt", "sng"])

cmd_html = pd.DataFrame({
    "start": [
        '<span class_val="hl def">', '<span class_val="hl kwb">', '<span class_val="hl num">', 
        '<span class_val="hl com">', '<span class_val="hl kwd">', '<span class_val="hl kwc">', 
        '<span class_val="hl kwa">', '<span class_val="hl opt">', '<span class_val="hl sng">'
    ],
    "end": ["</span>"] * 9,
    "token": ["def", "kwb", "num", "com", "kwd", "kwc", "kwa", "opt", "sng"]
}, index=["def", "kwb", "num", "com", "kwd", "kwc", "kwa", "opt", "sng"])

def custom_r_tokenizer(code):
    tokens = []
    pos = 0
    while pos < len(code):
        # Comments
        if code[pos] == '#':
            end = len(code)
            tokens.append((code[pos:end], 'com'))
            pos = end
            continue
        
        # Strings
        if code[pos] in ("'", '"'):
            quote = code[pos]
            end = code.find(quote, pos + 1)
            if end == -1: end = len(code)
            else: end += 1
            tokens.append((code[pos:end], 'sng'))
            pos = end
            continue

        # Keywords/Assignment
        if code.startswith('<-', pos):
            tokens.append(('<-', 'kwb'))
            pos += 2
            continue
        
        # Numbers
        match_num = re.match(r'\d+(\.\d+)?', code[pos:])
        if match_num:
            tokens.append((match_num.group(0), 'num'))
            pos += len(match_num.group(0))
            continue

        # R Keywords
        match_kwa = re.match(r'\b(function|for|if|else|break|repeat|while|in)\b', code[pos:])
        if match_kwa:
            tokens.append((match_kwa.group(0), 'kwa'))
            pos += len(match_kwa.group(0))
            continue

        # R Functions (Common ones)
        match_kwd = re.match(r'\b(print|c|list|q)\b', code[pos:])
        if match_kwd:
            tokens.append((match_kwd.group(0), 'kwd'))
            pos += len(match_kwd.group(0))
            continue

        # Special characters / Operators
        char = code[pos]
        if char in '(),{}=':
            tokens.append((char, 'def'))
            pos += 1
            continue
        if char in '@:<>':
            tokens.append((char, 'opt'))
            pos += 1
            continue
        
        # Identifiers
        match_id = re.match(r'\b[a-zA-Z_][a-zA-Z0-9_.]*\b', code[pos:])
        if match_id:
            text = match_id.group(0)
            # context-based classification for kwc (arguments, slots)
            is_kwc = False
            if tokens:
                prev_text, _ = tokens[-1]
                if prev_text in ('(', '=', '@'):
                    is_kwc = True
            
            tokens.append((text, 'kwc' if is_kwc else 'def'))
            pos += len(text)
            continue
        
        if char.isspace():
            tokens.append((char, 'space'))
            pos += 1
            continue

        tokens.append((char, 'def'))
        pos += 1
        
    return tokens

def apply_markup(tokens, format_val):
    markup = cmd_latex if format_val == "latex" else cmd_html
    result = []
    for text, token_type in tokens:
        if token_type == 'space':
            result.append(text)
            continue
        if token_type in markup.index:
            row = markup.loc[token_type]
            val = html.escape(text) if format_val == "html" else text
            if format_val == "latex" and token_type == 'sng':
                val = val.replace('{', r'\{').replace('}', r'\}')
            result.append(f"{row['start']}{val}{row['end']}")
        else:
            result.append(text)
    return "".join(result)

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if not code:
        return ""
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
    tokens = custom_r_tokenizer(code)
    return apply_markup(tokens, format_val)

# r2py:entity:cat
def hi_latex(texts):
    if isinstance(texts, str):
        texts = [texts]
    return "\n".join([hilight(t, format_val="latex") for t in texts])

# r2py:entity:cat_1
def hi_html(texts):
    if isinstance(texts, str):
        texts = [texts]
    return "\n".join([hilight(t, format_val="html") for t in texts])

# Execution
# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# r2py:entity:txt
txt = [
    "a <- 1 # something", 
    'c(y="world", z="hello")', 
    "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", 
    "z@child # S4 slot",
    "'special chars <>#$%&_{}'"
]

# r2py:entity:cat
print(hi_latex(txt))
# r2py:entity:cat_1
print(hi_html(txt))

# Ensure globals are present for verification
cmd_latex = cmd_latex
cmd_html = cmd_html