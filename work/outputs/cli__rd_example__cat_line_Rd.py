# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/cli__rd_example__cat_line_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'cli__rd_example__cat_line_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import colorama

colorama.init()

# Mapping colors to ANSI codes
COLORS = {
    "red": colorama.Fore.RED,
    "green": colorama.Fore.GREEN,
    "reset": colorama.Style.RESET_ALL
}

# Mapping R cli bullet names to characters
BULLETS = {
    "bullet": "•",
    "tick": "✔",
}

# r2py:entity:cat_line
def cat_line(*args, col="white", background_col=None, file=None):
    # R paste0(..., collapse="\n") - however, cat_line's use of paste0 
    # without a specified separator for the arguments means no spaces.
    # But the R source used "This is ", "a ", "line of text." (with spaces in strings).
    text = "".join(map(str, args))
    c_start = COLORS.get(col, "")
    c_end = COLORS["reset"]
    print(f"{c_start}{text}{c_end}", end="\n")

# r2py:entity:cat_bullet
def cat_bullet(*args, col="white", background_col=None, bullet="bullet", bullet_col="white", file=None):
    # R: paste0(...) joins the arguments into one string
    text = "".join(map(str, args))
    
    # Get bullet character
    b_char = BULLETS.get(bullet, BULLETS["bullet"])
    
    # Apply styles
    b_color = COLORS.get(bullet_col, "")
    b_reset = COLORS["reset"]
    
    # R: paste(bullet, out) adds a space between them
    formatted_bullet = f"{b_color}{b_char}{b_reset}"
    line_content = f"{formatted_bullet} {text}"
    
    # Use cat_line for the final output
    cat_line(line_content, col=col, background_col=background_col, file=file)

# r2py:entity:cat_rule
def cat_rule(*args, file=None):
    # R cat_rule produces a line of box-drawing characters \u2500
    # Usually fills the terminal width, but based on verification we need the specific character.
    rule_str = "\u2500" * 80 
    cat_line(rule_str, file=file)

# Translation of the execution block
import string

# r2py:entity:cat_line
cat_line("This is ", "a ", "line of text.", col="red")

# letters[1:5] in R is letters[0:5] in Python
cat_bullet(letters[0:5]) # This will pass a list to cat_bullet; in R cat_bullet(letters[1:5]) 
# treats the vector as multiple arguments if using ..., but here letters[1:5] is one object.
# However, cat_bullet is defined as function(..., ...), so a vector passed as the first arg 
# is treated as a single element unless it's splatted. In R, cat_bullet(letters[1:5]) 
# actually results in 5 bullets if the function handles vectors, but the R source 
# for cat_bullet provided uses paste0(...), which collapses the vector into one string.
# Let's adjust cat_bullet to handle lists to match R's vector behavior in paste0.

# r2py:entity:cat_bullet
def cat_bullet_fixed(*args, col="white", background_col=None, bullet="bullet", bullet_col="white", file=None):
    # Handle vectors/lists by joining them if they are passed as a single argument
    processed_args = []
    for arg in args:
        if isinstance(arg, list):
            processed_args.extend(arg)
        else:
            processed_args.append(arg)
    
    # For cat_bullet, if a vector is passed, R's cat_bullet usually iterates.
    # Looking at the verification: R produced 5 lines.
    # So cat_bullet must iterate over the items.
    
    # Re-evaluating cat_bullet logic based on verification output
    items = []
    for arg in args:
        if isinstance(arg, list): items.extend(arg)
        else: items.append(arg)
    
    b_char = BULLETS.get(bullet, BULLETS["bullet"])
    b_color = COLORS.get(bullet_col, "")
    b_reset = COLORS["reset"]
    
    for item in items:
        formatted_bullet = f"{b_color}{b_char}{b_reset}"
        cat_line(f"{formatted_bullet} {item}", col=col, background_col=background_col, file=file)

# Override the previous definition
cat_bullet = cat_bullet_fixed

# Execute calls
# cat_line was already called.
# r2py:entity:cat_bullet
cat_bullet(letters[0:5])
# r2py:entity:cat_bullet_1
cat_bullet(letters[0:5], bullet="tick", bullet_col="green")
# r2py:entity:cat_rule
cat_rule()