# Translated from <R script> by r2py v0.3.0
import pandas as pd
import re

# --- Mock highr internals ---

# R's cmd_latex and cmd_html provide the mapping for highlighting tokens.
# These are internal to highr.
cmd_latex = pd.DataFrame({
    "start": ["\\texttt{", ""],
    "end": ["}", ""],
}, index=["DEFAULT", "OTHER"])

cmd_html = pd.DataFrame({
    "start": ["<code>", ""],
    "end": ["</code>", ""],
}, index=["DEFAULT", "OTHER"])

def escape_latex(text):
    # Basic R-style latex escaping for highr
    res = text.replace("\\", "\\textbackslash{}")
    res = res.replace("_", "\\_").replace("#", "\\#").replace("&", "\\&").replace("%", "\\%")
    res = res.replace("{", "\\{").replace("}", "\\}")
    return res

def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")

def raw_string(x):
    if isinstance(x, list):
        return "\n".join(map(str, x))
    return str(x)

def valid_syntax(code, silent=False):
    return True

def tokenize_r(code):
    """
    Very simplified R tokenizer to simulate highr's behavior.
    """
    tokens = []
    # This is a crude approximation of R lexing for the example cases
    # Patterns: strings, comments, numbers, keywords, operators, identifiers
    patterns = [
        (r'#.*', 'com'),
        (r'".*?"|\'.*?\'', 'sng'),
        (r'\b(function|for|if|else|break|in)\b', 'kwa'),
        (r'\b(c|print)\b', 'kwd'),
        (r'\b\d+\b', 'num'),
        (r'<-|=', 'kwb'),
        (r'[:@<>]', 'opt'),
        (r'[a-zA-Z_][a-zA-Z0-9._]*', 'def'),
        (r'.', 'def'),
    ]
    
    combined_pattern = '|'.join(f'({p})' for p, t in patterns)
    for match in re.finditer(combined_pattern, code):
        for i, (p, t) in enumerate(patterns):
            if match.group(i + 1):
                tokens.append((match.group(i + 1), t))
                break
    return tokens

def hilight_one(code, format_val, markup, escape_fun):
    if isinstance(code, list):
        lines = code
    else:
        lines = [code]
    
    results = []
    for line in lines:
        tokens = tokenize_r(line)
        highlighted_line = []
        
        # highr uses tags like \hldef{...} for latex and <span class="hl def">...</span> for html
        for val, tag in tokens:
            if format_val == "latex":
                # Map tags to \hl{tag}{val}
                # R tags: com, sng, kwa, kwd, num, kwb, opt, def
                # Latex counterparts: \hlcom, \hlsng, \hlkwa, \hlkwd, \hlnum, \hlkwb, \hlopt, \hldef
                hl_tag = f"\\hl{tag}"
                # Special case for escaping strings in latex if they aren't already handled
                escaped_val = escape_latex(val)
                highlighted_line.append(f"{hl_tag}{{{escaped_val}}}")
            else:
                # HTML counterparts: <span class="hl tag">val</span>
                escaped_val = escape_html(val)
                highlighted_line.append(f'<span class="hl {tag}">{escaped_val}</span>')
        
        # Join tokens with space if there was whitespace in original? 
        # highr usually preserves spacing.
        # The simplified tokenizer above loses whitespace. Let's refine.
        
        # Refined approach: use re.split to keep delimiters (whitespace)
        parts = re.split(r'(\s+)', line)
        final_line = []
        for part in parts:
            if not part: continue
            if part.isspace():
                final_line.append(part)
            else:
                # Tokenize the non-space part
                sub_tokens = tokenize_r(part)
                for val, tag in sub_tokens:
                    if format_val == "latex":
                        final_line.append(f"\\hl{tag}{{{escape_latex(val)}}}")
                    else:
                        final_line.append(f'<span class="hl {tag}">{escape_html(val)}</span>')
        results.append("".join(final_line))
        
    return "\n".join(results)

def hi_naive(code, format_val, markup, escape_fun):
    std = markup.loc["DEFAULT"]
    text = raw_string(code)
    return f"{std['start']}{escape_fun(text)}{std['end']}"

# r2py:entity:hilight
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
    
    # Prompt logic simulation
    p1 = escape_fun(">")
    p2 = escape_fun("+")
    std = markup.loc["DEFAULT"]
    p1 = f"{std['start']}{p1}{std['end']}"
    p2 = f"{std['start']}{p2}{std['end']}"
    
    # simplified split_source
    lines = code.split("\n") if isinstance(code, str) else code
    highlighted_lines = hilight_one(lines, format_val, markup, escape_fun).split("\n")
    
    res = []
    for i, line in enumerate(highlighted_lines):
        prefix = p1 if i == 0 else p2
        res.append(f"{prefix}{line}")
        
    return raw_string(res)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# --- Actual script execution ---

# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# r2py:entity:txt
txt = ["a <- 1 # something", "c(y=\"world\", z=\"hello\")", "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", "z@child # S4 slot",
    "'special chars <>#$%&_{}'"]

# R: cat(hi_latex(txt), sep = "\n")
# hi_latex returns a string where each element of the vector was highlighted and joined by \n
# r2py:entity:cat
res_latex = hi_latex(txt)
print(res_latex)

# R: cat(hi_html(txt), sep = "\n")
# r2py:entity:cat_1
res_html = hi_html(txt)
print(res_html)

# the markup data frames
print(cmd_latex)
print(cmd_html)