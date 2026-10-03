# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import re

# Implementation of highr logic
cmd_latex = pd.DataFrame({
    "start": ["\\textcolor{blue}{", "\\textcolor{red}{", "\\textcolor{green}{", "\\textcolor{gray}{"],
    "end": ["}", "}", "}", "}"],
    "type": ["keyword", "string", "comment", "default"]
}).set_index("type")

cmd_html = pd.DataFrame({
    "start": ["<span style='color:blue'>", "<span style='color:red'>", "<span style='color:green'>", "<span style='color:gray'>"],
    "end": ["</span>", "</span>", "</span>", "</span>"],
    "type": ["keyword", "string", "comment", "default"]
}).set_index("type")

# Adding a DEFAULT row as expected by the R code logic
cmd_latex.loc["DEFAULT"] = ["", ""]
cmd_html.loc["DEFAULT"] = ["", ""]

def escape_latex(text):
    chars = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\~", "^": r"\^"}
    return "".join(chars.get(c, c) for c in text)

def escape_html(text):
    chars = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}
    return "".join(chars.get(c, c) for c in text)

def raw_string(x):
    if isinstance(x, list):
        return "\n".join(x)
    return str(x)

# r2py:entity:hilight
def hilight_one(code, format_val, markup, escape_fun):
    # Simplified lexer simulation for highr
    # This mimics the basic behavior of highlighting strings, comments, and keywords
    result = []
    i = 0
    while i < len(code):
        # Comment
        if code[i] == '#':
            start = markup.loc["comment", "start"]
            end = markup.loc["comment", "end"]
            result.append(f"{start}{escape_latex(code[i:]) if format_val == 'latex' else escape_html(code[i:])}{end}")
            break
        # String
        elif code[i] in ('"', "'"):
            quote = code[i]
            start_idx = i
            i += 1
            while i < len(code) and code[i] != quote:
                i += 1
            content = code[start_idx:i+1]
            start = markup.loc["string", "start"]
            end = markup.loc["string", "end"]
            result.append(f"{start}{escape_latex(content) if format_val == 'latex' else escape_html(content)}{end}")
            i += 1
            continue
        # Basic Keyword simulation
        elif code[i].isalpha():
            start_idx = i
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                i += 1
            word = code[start_idx:i]
            if word in ("function", "for", "if", "else", "break", "print", "c"):
                start = markup.loc["keyword", "start"]
                end = markup.loc["keyword", "end"]
                result.append(f"{start}{word}{end}")
            else:
                result.append(word)
            continue
        else:
            result.append(code[i])
            i += 1
    return "".join(result)

def hi_naive(code, format_val, markup, escape_fun):
    return escape_latex(code) if format_val == 'latex' else escape_html(code)

def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if not code:
        return raw_string(code)
    
    if markup is None:
        markup = cmd_latex if format_val == "latex" else cmd_html
    
    escape_fun = escape_latex if format_val == "latex" else escape_html
    
    # Simplified valid_syntax check
    if not fallback:
        fallback = False 
    
    if not prompt:
        if isinstance(code, list):
            res = [hilight_one(c, format_val, markup, escape_fun) if not fallback else hi_naive(c, format_val, markup, escape_fun) for c in code]
            return raw_string(res)
        else:
            return raw_string(hilight_one(code, format_val, markup, escape_fun) if not fallback else hi_naive(code, format_val, markup, escape_fun))
    
    # Prompt logic
    p1 = escape_fun("> ")
    p2 = escape_fun("+ ")
    std = markup.loc["DEFAULT"].values
    if not any(pd.isna(std)):
        p1 = f"{std[0]}{p1}{std[1]}"
        p2 = f"{std[0]}{p2}{std[1]}"
        
    # split_source simulated
    lines = code.split('\n') if isinstance(code, str) else code
    res = []
    for line in lines:
        highlighted = hilight_one(line, format_val, markup, escape_fun)
        res.append(highlighted)
    
    # Reconstruct with prompts
    final_lines = []
    for i, line in enumerate(res):
        prompt_prefix = p1 if i == 0 else p2
        final_lines.append(f"{prompt_prefix}{line}")
        
    return raw_string(final_lines)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# --- Start of Example Code ---
# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# r2py:entity:txt
txt = ["a <- 1 # something", "c(y=\"world\", z=\"hello\")", "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", "z@child # S4 slot",
    "'special chars <>#$%&_{}'"]

# r2py:entity:cat
print(hi_latex(txt), sep="\n")
# r2py:entity:cat_1
print(hi_html(txt), sep="\n")

# the markup data frames
print(cmd_latex)
print(cmd_html)