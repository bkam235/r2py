# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import re

# highr:::cmd_latex and highr:::cmd_html are internal data frames.
# r2py:entity:hilight
cmd_latex = pd.DataFrame({
    "start": ["\\hldef{", "\\hlkwb{", "\\hlnum{", "\\hlcom{", "\\hlkwa{", "\\hlkwd{", "\\hlsng{", "\\hlopt{"],
    "end": ["}", "}", "}", "}", "}", "}", "}", "}"],
}, index=["def", "kwb", "num", "com", "kwa", "kwd", "sng", "opt"])

cmd_html = pd.DataFrame({
    "start": ["<span class_val=\"hl def\">", "<span class_val=\"hl kwb\">", "<span class_val=\"hl num\">", "<span class_val=\"hl com\">", "<span class_val=\"hl kwa\">", "<span class_val=\"hl kwd\">", "<span class_val=\"hl sng\">", "<span class_val=\"hl opt\">"],
    "end": ["</span>", "</span>", "</span>", "</span>", "</span>", "</span>", "</span>", "</span>"],
}, index=["def", "kwb", "num", "com", "kwa", "kwd", "sng", "opt"])

def tokenize_r(code):
    # Refined tokenizer to handle spaces and specific R keywords
    tokens = []
    patterns = [
        ('com', r'#.*'),
        ('sng', r'\"[^\"]*\"|\'[^\']*\''),
        ('num', r'\b\d+(\.\d+)?\b'),
        ('kwb', r'<-|='),
        ('kwa', r'\b(if|else|for|while|function|break|next|return|in)\b'),
        ('kwd', r'\b(c|list|data\.frame|print|cat)\b'),
        ('opt', r'[:@<>]'),
        ('def', r'\b[a-zA-Z_][a-zA-Z0-9_.]*\b'),
    ]
    
    combined_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
    
    pos = 0
    while pos < len(code):
        match = re.search(combined_pattern, code[pos:])
        if not match:
            tokens.append(('default', code[pos]))
            pos += 1
            continue
        
        if match.start() > 0:
            tokens.append(('default', code[pos : pos + match.start()]))
        
        for name, value in match.groupdict().items():
            if value:
                tokens.append((name, value))
                break
        pos += match.end()
        
    return tokens

def apply_markup(tokens, format_val):
    markup = cmd_latex if format_val == "latex" else cmd_html
    result = []
    for token_type, value in tokens:
        if token_type in markup.index:
            start = markup.loc[token_type, "start"]
            end = markup.loc[token_type, "end"]
            if format_val == "latex":
                val = value.replace("_", "\\_").replace("{", "\\{").replace("}", "\\}")
            else:
                val = value.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
            result.append(f"{start}{val}{end}")
        else:
            result.append(value)
    return "".join(result)

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if not code:
        return ""
    
    if isinstance(code, list):
        lines = code
    else:
        lines = code.splitlines() if "\n" in code else [code]
        
    results = []
    for line in lines:
        tokens = tokenize_r(line)
        results.append(apply_markup(tokens, format_val))
        
    return "\n".join(results)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, **kwargs, format_val="latex")

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, **kwargs, format_val="html")

# Execution logic
# r2py:entity:hilight (call)
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