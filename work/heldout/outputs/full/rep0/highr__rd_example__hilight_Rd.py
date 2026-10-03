import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter
import pandas as pd
import html

# R's highr uses specific token names and wrappers.
# R output examples: \hldef{x}, \hlkwb{=}, \hlnum{1}, \hlcom{# assignment}
# HTML examples: <span class_val="hl def">a</span>

TOKEN_MAP = {
    "Name": "def",
    "Keyword": "kwa",
    "Keyword.Namespace": "kwd",
    "Operator": "kwb", 
    "Number": "num",
    "String": "sng",
    "Comment": "com",
    "Punctuation": "def",
}

class HighrLatexFormatter(Formatter):
    def format(self, token_type, value):
        # Special case for operators to match highr behavior
        if token_type == "Operator":
            if value in ("<-", "=", "->"):
                style = "kwb"
            else:
                style = "opt"
        elif token_type == "Keyword":
            style = "kwa"
        elif token_type == "Punctuation":
            style = "opt" if value == "@" else "def"
        else:
            style = TOKEN_MAP.get(token_type, "def")
        
        # Escape LaTeX special characters in the value
        val = value.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("_", "\\_").replace("&", "\\&").replace("%", "\\%")
        return f"\\hl{style}{{{val}}}"

    def render(self, tokens, **kwargs):
        # Pygments R lexer often creates tokens for spaces; highr preserves them as literal spaces
        res = []
        for tt, v in tokens:
            if tt == "Text":
                res.append(v)
            else:
                res.append(self.format(tt, v))
        return "".join(res)

class HighrHtmlFormatter(Formatter):
    def format(self, token_type, value):
        if token_type == "Operator":
            style = "kwb" if value in ("<-", "=", "->") else "opt"
        elif token_type == "Keyword":
            style = "kwa"
        elif token_type == "Punctuation":
            style = "opt" if value == "@" else "def"
        else:
            style = TOKEN_MAP.get(token_type, "def")
        
        # Escape HTML special characters
        val = html.escape(value)
        return f'<span class_val="hl {style}">{val}</span>'

    def render(self, tokens, **kwargs):
        res = []
        for tt, v in tokens:
            if tt == "Text":
                res.append(v)
            else:
                res.append(self.format(tt, v))
        return "".join(res)

# The R internal data frames
cmd_latex = pd.DataFrame(index=["DEFAULT"], columns=[0, 1]).fillna("")
cmd_latex.loc["DEFAULT"] = ["", ""]

cmd_html = pd.DataFrame(index=["DEFAULT"], columns=[0, 1]).fillna("")
cmd_html.loc["DEFAULT"] = ["", ""]

# Global options
options = {
    "prompt": "> ",
    "continue": "+ "
}

# r2py:entity:hilight
def hilight(code, format_val="latex", markup=None, prompt=False, fallback=False):
    if code is None or (isinstance(code, (list, pd.Series)) and len(code) == 0):
        return ""
    
    if isinstance(code, (list, pd.Series)):
        res = [hilight(line, format_val, markup, prompt, fallback) for line in code]
        return "\n".join(res)

    r_lexer = get_lexer_by_name("r")
    tokens = r_lexer.get_tokens(code)
    
    if format_val == "latex":
        formatter = HighrLatexFormatter()
    else:
        formatter = HighrHtmlFormatter()
        
    highlighted = formatter.render(tokens)
    
    if prompt:
        p1 = options["prompt"]
        p2 = options["continue"]
        std = cmd_latex.loc["DEFAULT"].values if format_val == "latex" else cmd_html.loc["DEFAULT"].values
        if any(pd.notna(std)) and std[0] != "":
            p1 = f"{std[0]}{p1}{std[1]}"
            p2 = f"{std[0]}{p2}{std[1]}"
        return f"{p1}{highlighted}"

    return highlighted

# r2py:entity:cat
def hi_latex(code, **kwargs):
    return hilight(code, **kwargs, format_val="latex")

# r2py:entity:cat_1
def hi_html(code, **kwargs):
    return hilight(code, **kwargs, format_val="html")

# Execute R script logic
# print(hilight("x=1 # assignment")) 
# The R source says hilight("x=1 # assignment") which prints via autoprint.
# We use print() here to match the behavior.
# r2py:entity:hilight
print(hilight("x=1 # assignment"))

# r2py:entity:txt
txt = [
    "a <- 1 # something", 
    "c(y=\"world\", z=\"hello\")", 
    "b=function(x=5) {",
    "for(i in 1:10) {\n  if (i < x) print(i) else break}}", 
    "z@child # S4 slot",
    "'special chars <>#$%&_{}'"
]

# cat(hi_latex(txt), sep = "\n")
# r2py:entity:cat
print(hi_latex(txt))
# cat(hi_html(txt), sep = "\n")
# r2py:entity:cat_1
print(hi_html(txt))

# the markup data frames
print(cmd_latex)
print(cmd_html)