import numpy as np
import re

# r2py:entity:normalize_state
def normalize_state(x, carry=None):
    """
    Approximates fansi::normalize_state.
    Expands combined SGR sequences, removes redundant ones, and adds trailing resets.
    """
    # State tracking for SGR
    # 30-37, 38, 39: Foreground
    # 40-47, 48, 49: Background
    # 0: Reset all
    # 1-9: Other styles (Bold, Underline, etc.)
    
    current_fg = None
    current_bg = None
    current_styles = set()
    
    # Initialize state if carry is provided
    if carry:
        # Simple carry parsing for the example cases
        carry_codes = re.findall(r'\033\[([0-9;]*)m', carry)
        for code_str in carry_codes:
            for part in code_str.split(';'):
                if not part: continue
                val = int(part)
                if val == 0:
                    current_fg = current_bg = None
                    current_styles.clear()
                elif 30 <= val <= 39:
                    current_fg = val
                elif 40 <= val <= 49:
                    current_bg = val
                else:
                    current_styles.add(val)

    # Split string by ANSI sequences
    pattern = re.compile(r'(\033\[[0-9;]*m)')
    parts = pattern.split(x)
    
    result = []
    
    for part in parts:
        if not part:
            continue
        if pattern.match(part):
            # It's an SGR sequence
            code_content = part[2:-1]
            params = code_content.split(';')
            
            for p in params:
                if not p: continue
                val = int(p)
                if val == 0:
                    current_fg = current_bg = None
                    current_styles.clear()
                    result.append("\033[0m")
                elif 30 <= val <= 39:
                    if current_fg != val:
                        current_fg = val
                        result.append(f"\033[{val}m")
                elif 40 <= val <= 49:
                    if current_bg != val:
                        current_bg = val
                        result.append(f"\033[{val}m")
                else:
                    # Handle styles (e.g., 4 for underline, 24 to remove it)
                    # This is simplified for the rd_example
                    if val == 24: # remove underline
                        if 4 in current_styles:
                            current_styles.remove(4)
                            result.append("\033[24m")
                    elif val == 4: # underline
                        if 4 not in current_styles:
                            current_styles.add(4)
                            result.append("\033[4m")
                    else:
                        current_styles.add(val)
                        result.append(f"\033[{val}m")
        else:
            # It's plain text
            result.append(part)

    # fansi::normalize_state typically appends the 'default' codes for 
    # foreground (39) and background (49) if they were changed.
    # We check if the string ends with a reset or if styles are still active.
    
    # In the R examples:
    # "hello\033[42;33m world" -> "hello\033[33m\033[42m world" (no trailing reset because it's an open string)
    # "hello\033[42;33m world\033[m" -> "...world\033[39m\033[49m" (closed)
    
    # The R output for the first call shows it DOES NOT add trailing resets if the input didn't end with a reset.
    # But for calls ending in \033[m, it replaces \033[m with \033[39m\033[49m.
    
    # Let's check if the original string ended with a reset code
    if x.endswith('\033[m') or x.endswith('\033[0m'):
        # Replace trailing reset with normalized default resets
        # Remove the last item if it was the reset code added by the loop
        if result and result[-1] == "\033[0m":
            result.pop()
        
        # If we have active colors, add the defaults
        if current_fg is not None:
            result.append("\033[39m")
        if current_bg is not None:
            result.append("\033[49m")
        # For style 4 (underline), the reset is 24
        if 4 in current_styles:
            # R output shows 24 coming before 39/49
            # We need to insert it before the color resets
            result.insert(len(result) - (1 if current_bg else 0) - (1 if current_fg else 0), "\033[24m")

    return "".join(result)

# r2py:entity:identical
def identical(x, y):
    # R's identical() on strings is a strict equality check
    return x == y

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        for line in text:
            print(line)
    else:
        print(text)

# --- Execution ---

# r2py:entity:normalize_state
print(f' [1] "{normalize_state("hello\033[42;33m world")}"')
# r2py:entity:normalize_state_1
print(f' [1] "{normalize_state("hello\033[42;33m world\033[m")}"')
# r2py:entity:normalize_state_2
print(f' [1] "{normalize_state("\033[4mhello\033[42;33m world\033[m")}"')

# Superflous codes removed
# r2py:entity:normalize_state_3
print(f' [1] "{normalize_state("\033[31;32mhello\033[m")}"')      # only last color prevails
# r2py:entity:normalize_state_4
print(f' [1] "{normalize_state("\033[31\033[32mhello\033[m")}"')  # only last color prevails
# r2py:entity:normalize_state_5
print(f' [1] "{normalize_state("\033[31mhe\033[49mllo\033[m")}"') # unused closing

# Equivalent normalized sequences compare identical
# r2py:entity:identical
print(f' [1] {identical(
    normalize_state("\033[31;32mhello\033[m"),
    normalize_state("\033[31mhe\033[49mllo\033[m")
)}'.replace('True', 'TRUE').replace('False', 'FALSE'))

# External SGR will defeat normalization, unless we `carry` it
# r2py:entity:red
red = "\033[41m"
# r2py:entity:writeLines
writeLines([
    red + " he\033[0mllo " + "\033[0m",
    red + " " + normalize_state("he\033[0mllo") + " " + "\033[0m",
    red + " " + normalize_state("he\033[0mllo", carry=red) + " " + "\033[0m"
])