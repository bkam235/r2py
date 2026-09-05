# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import colorama

colorama.init()
red = colorama.Fore.RED
reset = colorama.Style.RESET_ALL

# r2py:entity:col_align
def col_align(text, width, align="left"):
    formatted_text = f"{red}{text}{reset}"
    # Calculate visible length of text without ANSI codes
    visible_len = len(text)
    
    if align == "left":
        return formatted_text.ljust(width + (len(formatted_text) - visible_len))
    elif align == "right":
        return formatted_text.rjust(width + (len(formatted_text) - visible_len))
    elif align == "center":
        return formatted_text.center(width + (len(formatted_text) - visible_len))
    return formatted_text

# r2py:entity:col_align
print(col_align("foobar", 20, "left"))
# r2py:entity:col_align_1
print(col_align("foobar", 20, "center"))
# r2py:entity:col_align_2
print(col_align("foobar", 20, "right"))