# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import termcolor
from termcolor import colored

# Crayon equivalent using termcolor
# r2py:entity:str
str_val = (
# r2py:entity:red
    colored("I am red---", "red") + 
# r2py:entity:green
    colored("and I am green-", "green") + 
# r2py:entity:underline
    "\033[4mI underlined\033[0m"
)

# r2py:entity:cat
print(str_val)

# col_strsplit equivalent: split while preserving ANSI codes
# Using a regex that doesn't break on ANSI escape sequences
import re
# r2py:entity:cat_1
def col_strsplit(text, pattern):
    return re.split(pattern, text)

print("\n".join(col_strsplit(str_val, r"[-]+")))

# strip_style equivalent: remove ANSI escape codes
# r2py:entity:strsplit
def strip_style(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\].|[0-9-;]*[$-^YZ])')
    return ansi_escape.sub('', text)

print(re.split(r"[-]+", strip_style(str_val)))

# r2py:entity:cat_2
print(" ".join(col_strsplit(str_val, ""))) # Note: re.split("") returns empty strings
# r2py:entity:strsplit_1
print(list(strip_style(str_val)))