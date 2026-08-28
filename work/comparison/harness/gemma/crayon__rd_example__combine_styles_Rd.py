# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 10

from termcolor import colored

# Python's termcolor is the closest equivalent to crayon for ANSI styling.
# Note: 'bgCyan' is supported, 'red' is supported. 'bold' is a parameter.

# Example 1: bold, red, bgCyan
# r2py:entity:cat
print(colored("Warning!", "red", "on_cyan", attrs=["bold"]))

# Example 2: bold, red, bgCyan
# r2py:entity:cat_1
print(colored("Warning!", "red", "on_cyan", attrs=["bold"]))

# Example 3: bold, red, bgCyan
# r2py:entity:cat_2
print(colored("Warning!", "red", "on_cyan", attrs=["bold"]))

# Example 4: bold, red, bgCyan
# r2py:entity:cat_3
print(colored("Warning!", "red", "on_cyan", attrs=["bold"]))