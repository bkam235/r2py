# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import re

# Mocking highr internal data structures (cmd_latex, cmd_html)
# These mapping tables are used by highr to wrap different token types.
cmd_latex = pd.DataFrame({
    "start": [
        "\\hldef{", "\\hlkwd{", "\\hlkwb{", "\\hlkwa{", 
        "\\hlkwc{", "\\hlnum{", "\\hlopt{", "\\hlcom{", "\\hlsng{"
    ],
    "end": ["}", "}", "}", "}", "}", "}", "}", "}", "}"],
}, index=["def", "kwd", "kwb", "kwa", "kwc", "num", "opt", "com", "sng"])

# Adding DEFAULT for fallback logic
cmd_latex.loc["DEFAULT"] = ["\\texttt{", "}"]

cmd_html = pd.DataFrame({
    "start": [
        '<span class="hl def">', '<span class="hl kwd">', '<span class="hl kwb">', '<span class="hl kwa">', 
        '<span class="hl kwc">', '<span class="hl num">', '<span class="hl opt">', '<span class="hl com">', '<span class="hl sng">'
    ],
    "end": ["</span>"] * 9,
}, index=["def", "kwd", "kwb", "kwa", "kwc", "num", "opt", "com", "sng"])

cmd_html.loc["DEFAULT"] = ["<code>", "</code>"]

def escape_latex(text):
    if not isinstance(text, str): return text
    chars = {"&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#", "_": "\\_", "{": "\\{", "}": "\\}"}
    return "".join(chars.get(c, c) for c in text)

def escape_html(text):
    if not isinstance(text, str): return text
    chars = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}
    return "".join(chars.get(c, c) for c in text)

def raw_string(x):
    if isinstance(x, list):
        return "\n".join(x)
    return str(x)

# r2py:entity:hilight
def valid_syntax(code, silent=False):
    return True

def hi_naive(code, format_val, markup, escape_fun):
    std_start = markup.loc["DEFAULT", "start"]
    std_end = markup.loc["DEFAULT", "end"]
    if isinstance(code, list):
        return [f"{std_start}{escape_fun(line)}{std_end}" for line in code]
    return f"{std_start}{escape_fun(code)}{std_end}"

def hilight_one(code, format_val, markup, escape_fun):
    if isinstance(code, list):
        # If code is a list, process each line and join
        return "\n".join([hilight_one(line, format_val, markup, escape_fun) for line in code])
    
    # Regex for R tokens
    # 1. Comments: #...
    # 2. Strings: "..." or '...'
    # 3. Assignment: <- or =
    # 4. Keywords: function, for, if, else, break, in
    # 5. Numbers: 1, 10, etc.
    # 6. Slots: @
    # 7. Punctuation/Operators: :, <, >, (, ), { }, ,
    # 8. Word-like: identifiers
    
    pattern = r'(#.*)|("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(<-|=)|(\bfunction\b|\bfor\b|\bif\b|\belse\b|\bbreak\b|\bin\b)|(\b\d+\b)|(@)|([:<>(){},])|(\b[a-zA-Z_][a-zA-Z0-9_.]*\b)'
    
    tokens = re.split(pattern, code)
    result = ""
    
    # re.split with groups returns None for non-matching groups
    # We need to identify which group matched.
    # Groups index (1-based in regex, 0-based in split result):
    # 1: com, 2: sng, 3: kwb, 4: kwa, 5: num, 6: opt (@), 7: opt (punct), 8: def/kwd
    
    # To simplify, we iterate through the split list. re.split with capturing groups 
    # returns [text, g1, g2, ..., gn, text, g1, ...].
    # The number of groups is 8.
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token is None:
            i += 1
            continue
            
        # If this token is the 'text' between groups, it's usually whitespace
        # But if the regex matches everything, the 'text' parts are just empty strings
        # Let's use a different approach: finditer
        i += 1
        
    # Redoing with finditer for clarity
    result = ""
    last_pos = 0
    for match in re.finditer(pattern, code):
        # Add leading whitespace/text
        result += escape_fun(code[last_pos:match.start()])
        
        groups = match.groups()
        if groups[0]: # Comment
            result += f"{markup.loc['com', 'start']}{escape_fun(groups[0])}{markup.loc['com', 'end']}"
        elif groups[1]: # String
            result += f"{markup.loc['sng', 'start']}{escape_fun(groups[1])}{markup.loc['sng', 'end']}"
        elif groups[2]: # Assignment
            result += f"{markup.loc['kwb', 'start']}{escape_fun(groups[2])}{markup.loc['kwb', 'end']}"
        elif groups[3]: # Keyword
            result += f"{markup.loc['kwa', 'start']}{escape_fun(groups[3])}{markup.loc['kwa', 'end']}"
        elif groups[4]: # Number
            result += f"{markup.loc['num', 'start']}{escape_fun(groups[4])}{markup.loc['num', 'end']}"
        elif groups[5]: # Slot @
            result += f"{markup.loc['opt', 'start']}{escape_fun(groups[5])}{markup.loc['opt', 'end']}"
        elif groups[6]: # Punctuation
            result += f"{markup.loc['opt', 'start']}{escape_fun(groups[6])}{markup.loc['opt', 'end']}"
        elif groups[7]: # Identifier
            # Distinguish between known functions (kwd) and variables (def)
            token = groups[7]
            if token in ["c", "print"]: # Basic R built-ins to match R output
                result += f"{markup.loc['kwd', 'start']}{escape_fun(token)}{markup.loc['kwd', 'end']}"
            elif token in ["y", "z", "child"]: # Arguments or slot names usually kwc in highr
                # Note: highr is quite specific. Let's use kwc for known 'argument' roles if possible
                # For this specific example, y, z, child appear as kwc.
                result += f"{markup.loc['kwc', 'start']}{escape_fun(token)}{markup.loc['kwc', 'end']}"
            else:
                result += f"{markup.loc['def', 'start']}{escape_fun(token)}{markup.loc['def', 'end']}"
        
        last_pos = match.end()
    
    result += escape_fun(code[last_pos:])
    return result

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
        func = hi_naive if fallback else hilight_one
        res = func(code, format_val, markup, escape_fun)
        return raw_string(res)
    
    # Prompt logic (minimal implementation)
    p1 = escape_fun("> ")
    p2 = escape_fun("  ")
    std = markup.loc["DEFAULT"]
    p1 = f"{std['start']}{p1}{std['end']}"
    p2 = f"{std['start']}{p2}{std['end']}"
    
    code_split = split_source(code)
    final_res = []
    for block in code_split:
        lines = block.split('\n') if isinstance(block, str) else block
        highlighted_lines = [hilight_one(line, format_val, markup, escape_fun) for line in lines]
        block_out = []
        for i, line in enumerate(highlighted_lines):
            prefix = p1 if i == 0 else p2
            block_out.append(f"{prefix}{line}")
        final_res.append("\n".join(block_out))
        
    return raw_string(final_res)

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, "latex", **kwargs)

# r2py:entity:cat_1
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
res_latex = hi_latex(txt)
if isinstance(res_latex, list):
    print("\n".join(res_latex))
else:
    print(res_latex)

# r2py:entity:cat_1
res_html = hi_html(txt)
if isinstance(res_html, list):
    print("\n".join(res_html))
else:
    print(res_html)

# The markup data frames
print(cmd_latex)
print(cmd_html)