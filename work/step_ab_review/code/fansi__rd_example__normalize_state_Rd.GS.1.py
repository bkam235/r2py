import numpy as np
import re

# r2py:entity:normalize_state
def normalize_state(x, warn=True, term_cap=None, carry=None):
    """
    Approximates fansi::normalize_state.
    Normalizes ANSI escape sequences by expanding combined SGR codes and ensuring 
    state consistency.
    """
    # SGR categories
    # 30-37, 39: foreground
    # 40-47, 49: background
    # 0: reset
    
    # Extract all SGR sequences: \033[...m
    pattern = re.compile(r'(\033\[[0-9;]*m)')
    
    # We need to track the current state to determine what resets are needed at the end
    # foreground (fg), background (bg)
    current_fg = None
    current_bg = None
    
    # If carry is provided, it influences the starting state
    if carry:
        carry_matches = pattern.findall(carry)
        for match in carry_matches:
            params = match[2:-1].split(';')
            for p in params:
                if not p: continue
                val = int(p)
                if 30 <= val <= 39: current_fg = val
                elif 40 <= val <= 49: current_bg = val
                elif val == 0:
                    current_fg = 39
                    current_bg = 49

    parts = pattern.split(x)
    matches = pattern.findall(x)
    
    result_parts = []
    
    for i in range(len(parts)):
        result_parts.append(parts[i])
        if i < len(matches):
            match = matches[i]
            params = match[2:-1].split(';')
            
            # Expand combined sequences like \033[42;33m into \033[33m\033[42m
            # fansi typically orders them or handles them individually
            expanded = []
            for p in params:
                if not p: continue
                val = int(p)
                if val == 0:
                    current_fg = 39
                    current_bg = 49
                    expanded.append('\033[0m')
                elif 30 <= val <= 39:
                    current_fg = val
                    expanded.append(f'\033[{val}m')
                elif 40 <= val <= 49:
                    current_bg = val
                    expanded.append(f'\033[{val}m')
                else:
                    # Other SGR codes (like 4 for underline) are passed through
                    expanded.append(f'\033[{val}m')
            
            # fansi normalization for the provided examples:
            # if it's a simple color change, it might reorder or just append
            # Based on R output: "hello\033[33m\033[42m world"
            # We'll sort fg before bg for consistency with R's output
            fg_code = next((f'\033[{v}m' for v in params if v.isdigit() and 30 <= int(v) <= 39), None)
            bg_code = next((f'\033[{v}m' for v in params if v.isdigit() and 40 <= int(v) <= 49), None)
            
            if fg_code and bg_code and ';' in match:
                # Special case for combined color codes in R output
                result_parts[-1] = result_parts[-1] # do nothing, just add expanded
                result_parts.append(fg_code + bg_code)
            else:
                result_parts.append("".join(expanded))

    final_str = "".join(result_parts)
    
    # fansi::normalize_state appends resets if the string ends in a modified state
    # and the string didn't already end with a reset.
    # R output: "hello\033[33m\033[42m world\033[39m\033[49m"
    if not final_str.endswith('\033[0m'):
        resets = ""
        if current_fg is not None and current_fg != 39:
            resets += "\033[39m"
        if current_bg is not None and current_bg != 49:
            resets += "\033[49m"
        final_str += resets

    # Handle the 'carry' prefix in the final result
    prefix = carry if carry else ""
    return prefix + final_str

# r2py:entity:identical
def identical(x, y):
    return x == y

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        for line in text:
            print(line)
    else:
        print(text)

# --- Execution ---

# Note: R's print output for strings is usually [1] "string"
def r_print(val):
    print(f'[1] "{val}"')

# r2py:entity:normalize_state
r_print(normalize_state("hello\033[42;33m world"))
# r2py:entity:normalize_state_1
r_print(normalize_state("hello\033[42;33m world\033[m"))
# r2py:entity:normalize_state_2
r_print(normalize_state("\033[4mhello\033[42;33m world\033[m"))

# Superflous codes removed
# r2py:entity:normalize_state_3
r_print(normalize_state("\033[31;32mhello\033[m"))      # only last color prevails
# r2py:entity:normalize_state_4
r_print(normalize_state("\033[31\033[32mhello\033[m"))  # only last color prevails
# r2py:entity:normalize_state_5
r_print(normalize_state("\033[31mhe\033[49mllo\033[m")) # unused closing

# Equivalent normalized sequences compare identical
# r2py:entity:identical
# Note: R prints [1] FALSE/TRUE
print(f'[1] {str(identical(normalize_state("\033[31;32mhello\033[m"), normalize_state("\033[31mhe\033[49mllo\033[m"))).upper()}')

# External SGR will defeat normalization, unless we `carry` it
# r2py:entity:red
red = "\033[41m"
# r2py:entity:writeLines
writeLines([
    red + " he\033[0mllo " + "\033[0m",
    red + " " + normalize_state("he\033[0mllo") + " " + "\033[0m",
    red + " " + normalize_state("he\033[0mllo", carry=red) + " " + "\033[0m"
])