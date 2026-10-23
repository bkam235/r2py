# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import pandas as pd
import numpy as np

# r2py:entity:style_num
def style_num(x, negative=None, significant=None):
    # Simple substitute for pillar's number styling
    # In a real scenario, this would likely involve ANSI escape codes for colors
    result = []
    for i, val in enumerate(x):
        prefix = "-" if negative is not None and negative[i] else ""
        result.append(f"{prefix}{val}")
    return result

# r2py:entity:style_subtle
def style_subtle(text):
    # Substitute for dimming text
    return f"subtle({text})"

# r2py:entity:style_subtle_num
def style_subtle_num(x, negative=None):
    # Substitute for subtle number styling
    return [f"subtle({val})" for val in x]

# r2py:entity:style_bold
def style_bold(text):
    # Substitute for bolding text
    return f"bold({text})"

# r2py:entity:style_na
def style_na(text):
    # Substitute for NA styling
    return f"NA({text})"

# r2py:entity:style_neg
def style_neg(text):
    # Substitute for negative styling
    return f"-{text}"

# Execution
# r2py:entity:style_num
print(style_num(["123", "456"], negative=[True, False]))
# r2py:entity:style_num_1
print(style_num(["123", "456"], negative=[True, False], significant=[False, False]))
# r2py:entity:style_subtle
print(style_subtle("text"))
# r2py:entity:style_subtle_num
print(style_subtle_num(0.01 * np.arange(1, 4), negative=[True, False, True]))
# r2py:entity:style_bold
print(style_bold("Petal.Width"))
# r2py:entity:style_na
print(style_na("NA"))
# r2py:entity:style_neg
print(style_neg("123"))