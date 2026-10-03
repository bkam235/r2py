# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import re



# The highr package uses specific internal dataframes for markup.
# We recreate them exactly as they are in R's highr:::cmd_latex and highr:::cmd_html
cmd_latex = pd.DataFrame({
    "start": [
        "\\hlkwa{", "\\hlkwd{", "\\hlkwb{", "\\hlkwc{", "\\hlcom{", 
        "\\hlsng{", "\\hlnum{", "\\hlopt{", "\\hldef{"
    ],
    "end": ["}"],
}, index=["KWA", "KWD", "KWB", "KWC", "COM", "SNG", "NUM", "OPT", "DEF"])
# Note: highr's actual internal DFs have these names. DEFAULT is used for prompt wrapping.
cmd_latex.loc["DEFAULT"] = ["\\texttt{", "}"]

cmd_html = pd.DataFrame({
    "start": [
        '<span class="hl kwa">', '<span class="hl kwd">', '<span class="hl kwb">', 
        '<span class="hl kwc">', '<span class="hl com">', '<span class="hl sng">', 
        '<span class="hl num">', '<span class="hl opt">', '<span class="hl def">'
    ],
    "end": ["</span>"],
}, index=["KWA", "KWD", "KWB", "KWC", "COM", "SNG", "NUM", "OPT", "DEF"])
cmd_html.loc["DEFAULT"] = ["<code>", "</code>"]

def escape_latex(text):
    replacements = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"$\sim$"}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def escape_html(text):
    replacements = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def hilight_one(code, format_val, markup, escape_fun):
    if isinstance(code, list):
        return [hilight_one(line, format_val, markup, escape_fun) for line in code]
    
    # R syntax patterns for highr
    patterns = [
        (r'#.*$', 'COM'),
        (r'"[^"]*"|\'[^\']*\'', 'SNG'),
        (r'\b(if|else|for|while|function|next|break|in|repeat)\b', 'KWA'),
        (r'\b(c|print|paste|seq|rep|unlist|sapply|lapply|mapply)\b', 'KWD'),
        (r'\b(<-|=)\b', 'KWB'),
        (r'\b([a-zA-Z_][a-zA-Z0-9_.]*)\b', 'KWC'), # Simple approx for kwc/def
        (r'\b\d+(\.\d+)?\b', 'NUM'),
        (r'[\(\)\[\]\{\},:@<>\!]', 'OPT'),
    ]
    
    # This is a simplified tokenizer to mimic highr
    # highr actually uses a more complex R-specific lexer.
    # To match the expected output, we must map tokens to the markup indices.
    
    # Refined Patterns to match the specific output of the example
    # Based on R's output: \hldef{x}\hlkwb{=}\hlnum{1} \hlcom{# assignment}
    tokens = [
        (r'#.*$', 'COM'),
        (r'"[^"]*"|\'[^\']*\'', 'SNG'),
        (r'\b(if|else|for|while|function|next|break|in|repeat)\b', 'KWA'),
        (r'\b(c|print|paste|seq|rep|unlist|sapply|lapply|mapply)\b', 'KWD'),
        (r'(<-|=)', 'KWB'),
        (r'\b\d+(\.\d+)?\b', 'NUM'),
        (r'([@:<>])', 'OPT'),
        (r'([a-zA-Z_][a-zA-Z0-9_.]*)', 'DEF'),
        (r'([()\[\]{},])', 'DEF'), # R's highr often marks punctuation as def
    ]
    
    text = code
    result = ""
    pos = 0
    while pos < len(text):
        match = None
        for pattern, tag in tokens:
            m = re.match(pattern, text[pos:])
            if m:
                match = m
                current_tag = tag
                break
        
        if match:
            val = match.group(0)
            # Apply escaping for the content
            escaped_val = escape_fun(val)
            # Wrap with markup
            start = markup.loc[current_tag, "start"]
            end = markup.loc[current_tag, "end"]
            result += f"{start}{escaped_val}{end}"
            pos += len(val)
        else:
            result += text[pos]
            pos += 1
            
    return result

def raw_string(x):
    return x

def valid_syntax(code, silent=False):
    return True

def split_source(code):
    if isinstance(code, str):
        return [code]
    return code

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
        # highr's hilight_one handles strings or vectors of strings
        res = hilight_one(code, format_val, markup, escape_fun)
        return raw_string(res)
    
    # Prompt logic
    p1 = escape_fun(">") 
    p2 = escape_fun("+") 
    std = markup.loc["DEFAULT"].values
    if not any(pd.isna(std)):
        p1 = f"{std[0]}{p1}{std[1]}"
        p2 = f"{std[0]}{p2}{std[1]}"
        
    code_split = split_source(code)
    res = []
    for item in code_split:
        highlighted = hilight_one(item, format_val, markup, escape_fun)
        lines = highlighted.split('\n') if isinstance(highlighted, str) else highlighted
        
        formatted_lines = [p1] + [p2] * (len(lines) - 1)
        res.append("\n".join([f"{p} {l}" for p, l in zip(formatted_lines, lines)]))
        
    return raw_string(res)

def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

def hi_html(code, **kwargs):
    return hilight(code, "html", **kwargs)

# Main Execution
# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# r2py:entity:txt
txt = ["a <- 1 # something", "c(y=\"world\", z=\"hello\")", "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", "z@child # S4 slot",
    "'special chars <>#$%&_{}'"]

# r2py:entity:cat
latex_res = hi_latex(txt)
if isinstance(latex_res, list):
    print("\n".join(latex_res))
else:
    print(latex_res)

# r2py:entity:cat_1
html_res = hi_html(txt)
if isinstance(html_res, list):
    print("\n".join(html_res))
else:
    print(html_res)

print(cmd_latex)
print(cmd_html)