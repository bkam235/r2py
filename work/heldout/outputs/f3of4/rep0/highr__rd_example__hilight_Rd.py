# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import re

# Markup data frames simulating highr's internal tables
cmd_latex = pd.DataFrame({
    "start": ["\\hl", "\\hl"],
    "end": ["}", "}"],
}, index=["DEFAULT", "OTHER"])

cmd_html = pd.DataFrame({
    "start": ["<span class_val=\"hl ", "<span class_val=\"hl "],
    "end": ["></span>", "></span>"],
}, index=["DEFAULT", "OTHER"])

def escape_latex(s):
    # Basic LaTeX escaping for code snippets
    return s.replace("_", "\\_").replace("{", "\\{").replace("}", "\\}").replace("%", "\\%")

def escape_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# r2py:entity:hilight
def hilight_one(code, format_val, markup, escape_fun):
    # highr tokenizer logic approximation
    # Tokens: com (comment), sng (string), kwa (keyword a), kwd (keyword d), 
    # kwb (keyword b/assignment), num (number), kwc (keyword c/args), def (default/identifier), opt (operator)
    
    tokens = []
    pos = 0
    while pos < len(code):
        # Comment
        if code[pos] == '#':
            match = re.match(r'#.*', code[pos:])
            tokens.append(('com', match.group(0)))
            pos += len(match.group(0))
            continue
        
        # String
        if code[pos] in ("'", '"'):
            quote = code[pos]
            # Simplified string match (non-greedy)
            match = re.match(rf'{quote}.*?{quote}', code[pos:])
            if match:
                tokens.append(('sng', match.group(0)))
                pos += len(match.group(0))
                continue
        
        # Assignment (R's highr treats <- as kwb, but = as def or kwb depending on context)
        if code.startswith('<-', pos):
            tokens.append(('kwb', '<-'))
            pos += 2
            continue
        
        # Keywords (a)
        kwa_match = re.match(r'\b(function|for|if|else|break|in)\b', code[pos:])
        if kwa_match:
            tokens.append(('kwa', kwa_match.group(0)))
            pos += len(kwa_match.group(0))
            continue
            
        # Keywords (d) - functions like c(), print()
        kwd_match = re.match(r'\b(c|print)\b', code[pos:])
        if kwd_match:
            tokens.append(('kwd', kwd_match.group(0)))
            pos += len(kwd_match.group(0))
            continue
            
        # Numbers
        num_match = re.match(r'\b\d+\b', code[pos:])
        if num_match:
            tokens.append(('num', num_match.group(0)))
            pos += len(num_match.group(0))
            continue
            
        # Identifiers / Args
        id_match = re.match(r'\b[a-zA-Z_][a-zA-Z0-9_.]*\b', code[pos:])
        if id_match:
            text = id_match.group(0)
            # Heuristic for kwc: follows '(' or ',' or '='
            is_kwc = False
            if pos > 0:
                prev = code[pos-1]
                if prev in ('(', ',', '='):
                    is_kwc = True
            
            token_type = 'kwc' if is_kwc else 'def'
            tokens.append((token_type, text))
            pos += len(text)
            continue
            
        # Operators/Punctuation
        if code[pos] == '=':
            # In R highr, = is often treated as 'def' when it's an argument assignment
            # unless it's a top-level assignment.
            tokens.append(('def', '='))
            pos += 1
            continue
        if code[pos] in '@:<>{}[]':
            tokens.append(('opt', code[pos]))
            pos += 1
            continue
        if code[pos] in '(),':
            tokens.append(('def', code[pos]))
            pos += 1
            continue
            
        # Default / Whitespace
        tokens.append(('def', code[pos]))
        pos += 1

    # Formatting phase
    result = ""
    for t_type, t_text in tokens:
        if t_type == 'def' and t_text.isspace():
            result += t_text
        else:
            if format_val == "latex":
                val = escape_fun(t_text) if t_type == 'sng' else t_text
                # R's highr outputs \hltype{text}
                result += f"\\hl{t_type}{{{val}}}"
            else:
                # HTML: <span class_val="hl type">text</span>
                val = escape_fun(t_text)
                result += f'<span class_val="hl {t_type}">{val}</span>'
                
    return result

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if not code:
        return ""
    
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
        
    escape_fun = escape_latex if format_val == "latex" else escape_html
    
    if isinstance(code, list):
        res = [hilight_one(line, format_val, markup, escape_fun) for line in code]
        return "\n".join(res)
    
    return hilight_one(code, format_val, markup, escape_fun)

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

# Ensure globals for the data frames are present
cmd_latex = cmd_latex
cmd_html = cmd_html