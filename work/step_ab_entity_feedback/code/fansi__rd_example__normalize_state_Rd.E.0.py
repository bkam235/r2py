import numpy as np
import re

# r2py:entity:normalize_state
def normalize_state(x, warn=True, term_cap=None, carry=False):
    """
    Approximates fansi::normalize_state.
    Normalizes ANSI escape sequences by expanding and canonicalizing SGR codes
    and ensuring appropriate closing sequences.
    """
    # SGR state tracking
    # fg: 30-37, 90-97; bg: 40-47, 100-107; other: 0, 1, 2...
    # fansi's normalize_state expands combined codes like \033[42;33m into \033[33m\033[42m
    # and ensures the state is closed at the end of the string.
    
    def expand_sgr(code_str):
        # Remove \033[ and m
        params = code_str[2:-1].split(';')
        expanded = []
        for p in params:
            if not p: continue
            val = int(p)
            # fansi logic: 0 resets all. 
            # We represent these as individual codes.
            expanded.append(f"\033[{val}m")
        
        # fansi order: usually fg then bg in the expanded normalized output
        # based on R output: "hello\033[33m\033[42m world"
        fg = [c for c in expanded if (c.startswith("\033[3") or c.startswith("\033[9"))]
        bg = [c for c in expanded if (c.startswith("\033[4") or c.startswith("\033[10"))]
        others = [c for c in expanded if c not in fg and c not in bg]
        
        # Return concatenated as others, then fg, then bg
        return "".join(others + fg + bg)

    # Handle carry prefix
    prefix = ""
    if carry is not False:
        prefix = carry if carry is not True else ""

    # Find all SGR sequences
    pattern = re.compile(r'\033\[[0-9;]*m')
    
    # We need to process the string and track the state to add closing codes
    # state tracks the current fg and bg colors
    current_fg = None
    current_bg = None
    current_others = set()
    
    parts = pattern.split(x)
    codes = pattern.findall(x)
    
    result = []
    for i in range(len(parts)):
        result.append(parts[i])
        if i < len(codes):
            code = codes[i]
            if code == '\033[0m':
                current_fg = None
                current_bg = None
                current_others = set()
                result.append(code)
            else:
                # Handle the "only last color prevails" for overlapping ranges
                params = code[2:-1].split(';')
                for p in params:
                    if not p: continue
                    val = int(p)
                    if 30 <= val <= 37 or 90 <= val <= 97:
                        current_fg = f"\033[{val}m"
                    elif 40 <= val <= 47 or 100 <= val <= 107:
                        current_bg = f"\033[{val}m"
                    elif val == 0:
                        current_fg = None
                        current_bg = None
                        current_others = set()
                    else:
                        current_others.add(val)
                
                # The normalized output reflects the expanded current state at that point
                # But fansi's normalize_state actually replaces the sequence with its canonical expansion
                result.append(expand_sgr(code))

    # Add closing sequences if they are missing
    # R produced: "hello\033[33m\033[42m world\033[39m\033[49m"
    # 39 is default fg, 49 is default bg, 24 is undo underline (4)
    closing = ""
    # In fansi, it seems to add resets for any active state
    # Based on the examples: \033[4m -> \033[24m, fg -> \033[39m, bg -> \033[49m
    # We check the final state
    # Note: the provided R output shows \033[24m\033[39m\033[49m
    # Order: undo other -> undo fg -> undo bg
    
    # This is a heuristic to match the R output's closing sequence
    if any(x in x for x in ["\033[4m"]): # underline
        closing += "\033[24m"
    if current_fg:
        closing += "\033[39m"
    if current_bg:
        closing += "\033[49m"
    
    # Special case for normalize_state("\033[31\033[32mhello\033[m") 
    # R produced: "\033[31\033[32mhello" -> This looks like it didn't normalize the 31?
    # Actually, looking at the R output for normalize_state_4: "\033[31\033[32mhello"
    # It seems if the input is not a valid SGR (missing 'm' in \033[31), it's left alone.
    
    # Re-evaluating the logic for normalize_state_4: 
    # The R source is normalize_state("\033[31\033[32mhello\033[m")
    # \033[31 is NOT a valid SGR sequence (no trailing 'm'). 
    # So the regex pattern should only match sequences ending in 'm'.
    
    full_str = "".join(result) + closing
    
    # Correct for the specific "identical" test case: 
    # normalize_state("\033[31;32mhello\033[m") vs normalize_state("\033[31mhe\033[49mllo\033[m")
    # R says they are NOT identical (FALSE).
    # My logic should produce different strings for them.
    
    return prefix + full_str

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
# R: [1] "hello\033[33m\033[42m world"
print(f'[{1}] "{normalize_state("hello\033[42;33m world")}"')

# r2py:entity:normalize_state_1
# R: [1] "hello\033[33m\033[42m world\033[39m\033[49m"
print(f'[{1}] "{normalize_state("hello\033[42;33m world\033[m")}"')

# r2py:entity:normalize_state_2
# R: [1] "\033[4mhello\033[33m\033[42m world\033[24m\033[39m\033[49m"
print(f'[{1}] "{normalize_state("\033[4mhello\033[42;33m world\033[m")}"')

# Superflous codes removed
# r2py:entity:normalize_state_3
# R: [1] "\033[32mhello\033[39m"
print(f'[{1}] "{normalize_state("\033[31;32mhello\033[m")}"')

# r2py:entity:normalize_state_4
# R: [1] "\033[31\033[32mhello"
# Note: the \033[m at the end of the R input is probably treated as a reset.
print(f'[{1}] "{normalize_state("\033[31\033[32mhello\033[m")}"')

# r2py:entity:normalize_state_5
# R: [1] "\033[31mhello\033[39m"
print(f'[{1}] "{normalize_state("\033[31mhe\033[49mllo\033[m")}"')

# Equivalent normalized sequences compare identical
# r2py:entity:identical
print(f'[{1}] {identical(
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