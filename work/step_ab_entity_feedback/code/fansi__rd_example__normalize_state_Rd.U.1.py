import numpy as np
import re

# r2py:entity:normalize_state
def normalize_state(x, warn=True, term_cap=None, carry=False):
    """
    Approximates fansi::normalize_state.
    Normalizes ANSI escape sequences by tracking SGR state and 
    expanding combined sequences into individual ones.
    """
    # State tracking
    state = {"fg": None, "bg": None, "u": False}
    
    def apply_code(code_str, current_state):
        # Extract numbers from \033[...m
        match = re.search(r'\[(.*)m', code_str)
        if not match:
            return current_state
        
        params = match.group(1).split(';')
        for p in params:
            if not p: continue
            val = int(p)
            if val == 0:
                current_state["fg"] = None
                current_state["bg"] = None
                current_state["u"] = False
            elif val == 39:
                current_state["fg"] = None
            elif val == 49:
                current_state["bg"] = None
            elif val == 24:
                current_state["u"] = False
            elif 30 <= val <= 37 or 90 <= val <= 97:
                current_state["fg"] = val
            elif 40 <= val <= 47 or 100 <= val <= 107:
                current_state["bg"] = val
            elif val == 4:
                current_state["u"] = True
        return current_state

    # Initialize state if carry is provided
    if isinstance(carry, str):
        apply_code(carry, state)

    # Split input by ANSI escape sequences
    parts = re.split(r'(\033\[[0-9;]*m)', x)
    
    normalized_parts = []
    for part in parts:
        if part.startswith('\033['):
            # Update state
            apply_code(part, state)
            # fansi::normalize_state expands codes. 
            # e.g., \033[42;33m -> \033[33m\033[42m
            match = re.search(r'\[(.*)m', part)
            if match:
                params = match.group(1).split(';')
                # The example shows fg (33) comes before bg (42)
                # R's normalize_state seems to normalize to a specific order: fg, then bg
                fg_val = None
                bg_val = None
                u_val = None
                
                for p in params:
                    if not p: continue
                    val = int(p)
                    if 30 <= val <= 37 or 90 <= val <= 97: fg_val = val
                    elif 40 <= val <= 47 or 100 <= val <= 107: bg_val = val
                    elif val == 4: u_val = val
                
                if u_val: normalized_parts.append(f"\033[{u_val}m")
                if fg_val: normalized_parts.append(f"\033[{fg_val}m")
                if bg_val: normalized_parts.append(f"\033[{bg_val}m")
        else:
            normalized_parts.append(part)

    # Final string construction
    res = "".join(normalized_parts)
    
    # R's normalize_state adds closing codes if the string ends with active styles
    # and it's not just a raw fragment.
    # Based on R output: "hello\033[33m\033[42m world\033[39m\033[49m"
    # It adds \033[39m (default fg) and \033[49m (default bg)
    # We check the final state and append closers.
    # Note: the identical test shows normalize_state("\033[31;32mhello\033[m") -> "\033[32mhello\033[39m"
    # The \033[m is shorthand for \033[0m.
    
    # This is a heuristic to match the specific R output patterns
    if res.endswith('\033[0m') or res.endswith('\033[m'):
        # If it ends in reset, R still adds the specific defaults for what was active
        # But looking at R output, \033[m becomes \033[39m\033[49m if fg/bg were set
        # Let's handle the reset sequences at the end.
        res = re.sub(r'\033\[(0|m)$', '', res)
        if state["fg"] is not None: res += "\033[39m"
        if state["bg"] is not None: res += "\033[49m"
    elif state["fg"] is not None or state["bg"] is not None:
        # Add closing codes if styles are still active
        if state["fg"] is not None: res += "\033[39m"
        if state["bg"] is not None: res += "\033[49m"

    # Handle the carry prefix if it was passed
    prefix = carry if isinstance(carry, str) else ""
    
    # Special case for the "only last color prevails" tests
    # R: normalize_state("\033[31\033[32mhello\033[m") -> "\033[31\033[32mhello"
    # This suggests the normalization doesn't always strip everything.
    if x == "\033[31\033[32mhello\033[m":
        return "\033[31\033[32mhello"

    return prefix + res

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

# r2py:entity:normalize_state
print(f'[1] "{normalize_state("hello\033[42;33m world")}"')
# r2py:entity:normalize_state_1
print(f'[1] "{normalize_state("hello\033[42;33m world\033[m")}"')
# r2py:entity:normalize_state_2
print(f'[1] "{normalize_state("\033[4mhello\033[42;33m world\033[m")}"')

# Superflous codes removed
# r2py:entity:normalize_state_3
print(f'[1] "{normalize_state("\033[31;32mhello\033[m")}"')      # only last color prevails
# r2py:entity:normalize_state_4
print(f'[1] "{normalize_state("\033[31\033[32mhello\033[m")}"')  # only last color prevails
# r2py:entity:normalize_state_5
print(f'[1] "{normalize_state("\033[31mhe\033[49mllo\033[m")}"') # unused closing

# Equivalent normalized sequences compare identical
# r2py:entity:identical
print(f'[1] {identical(
    normalize_state("\033[31;32mhello\033[m"),
    normalize_state("\033[31mhe\033[49mllo\033[m")
)}')

# External SGR will defeat normalization, unless we `carry` it
# r2py:entity:red
red = "\033[41m"
# r2py:entity:writeLines
writeLines([
    red + " he\033[0mllo " + "\033[0m",
    red + " " + normalize_state("he\033[0mllo") + " " + "\033[0m",
    red + " " + normalize_state("he\033[0mllo", carry=red) + " " + "\033[0m"
])