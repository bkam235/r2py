import sys

# Simulating crayon's global state for styles
class CrayonState:
    def __init__(self):
        self.my_styles = {}

data_env = CrayonState()

# r2py:entity:names
def styles():
    """Return the current custom styles."""
    return data_env.my_styles

# r2py:entity:drop_style
def drop_style(style_name):
    """Remove a style from the registry."""
    if style_name in data_env.my_styles:
        del data_env.my_styles[style_name]

# r2py:entity:make_style
def make_style(**kwargs):
    """
    Simulates R's make_style.
    In R, make_style(new_style = "maroon", bg = TRUE) 
    1. Defines a style named 'new_style'.
    2. Returns a function (crayon object) that applies that style.
    3. Prints a confirmation message.
    """
    # Extract the style definition (first positional/named arg not bg/grey/colors)
    style_def = None
    style_name = None
    
    # Handle the ... logic to find the style definition and its name
    # In the call make_style(new_style = "maroon", bg = TRUE), 
    # 'new_style' is the name, 'maroon' is the value.
    for k, v in kwargs.items():
        if k not in ('bg', 'grey', 'colors'):
            style_name = k
            style_def = v
            break
            
    # Simulate the auto-print behavior of make_style in R
    # R output: "Crayon style function, new_style: example output."
    print(f"Crayon style function, {style_name}: example output.")
    
    # Store in the registry (simulating define_style)
    # We store a simple identifier or ANSI code; here we just track the name
    data_env.my_styles[style_name] = style_def
    
    # Return a "crayon" object (a closure that applies the style)
    def crayon_func(text):
        # Simplified: just returning text as we aren't implementing the full ANSI engine
        # but the structure mimics the R function return
        return text
    
    return crayon_func

# r2py:entity:cat
def style(string, as_val=None, bg_val=None):
    """Simulates crayon::style()"""
    # This is a simplification of use_or_make_style and the wrapping logic
    # In R, style("I am maroon", "new_style") applies the 'new_style' to the string.
    # If 'new_style' exists in styles(), it uses it.
    if as_val and as_val in styles():
        # Simulate applying the custom style
        return f"{string}" 
    return string

# Execution
# suppressPackageStartupMessages(library(crayon))
# (No-op in Python)

# make_style(new_style = "maroon", bg = TRUE)
# r2py:entity:make_style
make_style(new_style="maroon", bg=True)

# cat(style("I am maroon", "new_style"), "\n")
# r2py:entity:cat
print(style("I am maroon", "new_style"), end="\n")

# drop_style("new_style")
# r2py:entity:drop_style
drop_style("new_style")

# "new_style" %in% names(styles())
# R prints [1] FALSE for logicals
# r2py:entity:names
result = "new_style" in styles()
print(f"[1] {str(result).upper()}")