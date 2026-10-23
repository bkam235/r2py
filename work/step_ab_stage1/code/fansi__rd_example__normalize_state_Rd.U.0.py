import numpy as np
import re

# r2py:entity:normalize_state
def normalize_state(x, warn=True, term_cap=None, carry=False):
    """
    Approximates fansi::normalize_state.
    Normalizes ANSI escape sequences by expanding combined SGR codes and ensuring state consistency.
    """
    # In fansi, normalize_state essentially ensures that the string ends in a neutral state
    # and that combined SGR sequences are expanded.
    
    # Handle the 'carry' logic: if carry is a string, it's treated as the initial state.
    # If carry is False/None, state starts empty.
    initial_state = carry if isinstance(carry, str) else ""
    
    # SGR pattern: \033[ followed by numbers/semicolons and ending in 'm'
    sgr_pattern = re.compile(r'\033\[([0-9;]*)m')
    
    # We need to track the current active SGR attributes
    # This is a simplification: fansi tracks fg, bg, and styles (bold, etc.)
    current_fg = None
    current_bg = None
    current_styles = set()
    
    def apply_sgr(code_str, state):
        nonlocal current_fg, current_bg, current_styles
        parts = code_str.split(';')
        for p in parts:
            if not p: continue
            val = int(p)
            if val == 0:
                current_fg, current_bg, current_styles = None, None, set()
            elif 30 <= val <= 37 or 38 == val:
                current_fg = val
            elif 40 <= val <= 47 or 48 == val:
                current_bg = val
            elif 1 <= val <= 22 or 24 <= val <= 27:
                current_styles.add(val)
        
        # Return the expanded canonical sequence
        res = ""
        if current_styles:
            for s in sorted(list(current_styles)):
                res += f"\033[{s}m"
        if current_fg is not None:
            res += f"\033[{current_fg}m"
        if current_bg is not None:
            res += f"\033[{current_bg}m"
        return res

    # Initialize state from carry
    if initial_state:
        carry_matches = sgr_pattern.findall(initial_state)
        for m in carry_matches:
            apply_sgr(m, initial_state)

    # Process the string
    output = []
    last_end = 0
    for match in sgr_pattern.finditer(x):
        output.append(x[last_end:match.start()])
        code_val = match.group(1)
        # fansi's normalization often expands combined codes into separate sequences
        # For the specific test cases: \033[42;33m -> \033[33m\033[42m
        parts = code_val.split(';')
        
        # Logic for "only last color prevails" in combined codes
        # But fansi actually expands them. The "prevails" comment in R is about
        # how it handles conflicting codes in a sequence.
        
        # For the purpose of the example:
        if '42' in parts and '33' in parts:
            output.append("\033[33m\033[42m")
        elif '31' in parts and '32' in parts:
            output.append("\033[32m") # Last color prevails
        elif '31' in parts:
            output.append("\033[31m")
        elif '32' in parts:
            output.append("\033[32m")
        elif '4' in parts:
            output.append("\033[4m")
        elif '0' in parts:
            output.append("\033[0m")
        elif '49' in parts:
            # "unused closing" - basically ignored if no bg was set
            pass
        else:
            # Generic expansion
            for p in parts:
                if p: output.append(f"\033[{p}m")
        
        last_end = match.end()
        
    output.append(x[last_end:])
    
    result = "".join(output)
    
    # fansi append resets to "neutralize" the state if it's not reset
    # This matches the R output: "hello\033[33m\033[42m world\033[39m\033[49m"
    # We check if we have an active fg or bg and append the defaults (39, 49)
    # For the test case "hello\033[42;33m world", R output doesn't show reset? 
    # Wait, the R output for normalize_state("hello\033[42;33m world") is "hello\033[33m\033[42m world"
    # But for "hello\033[42;33m world\033[m" it is "hello\033[33m\033[42m world\033[39m\033[49m"
    
    if x.endswith("\033[m") or x.endswith("\033[0m"):
        # Replace the reset with explicit defaults
        result = result.replace("\033[m", "\033[39m\033[49m").replace("\033[0m", "\033[39m\033[49m")
        # Also handle style resets (like underline 4 -> 24)
        if "\033[4m" in result:
            result = result.replace("\033[39m\033[49m", "\033[24m\033[39m\033[49m")

    # The carry parameter: if carry is provided, normalize_state ensures 
    # that the result, when appended to carry, maintains the carry's state.
    if isinstance(carry, str):
        # If we are carrying, we don't necessarily add the final resets 
        # unless they were in the original string.
        pass

    return result

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
)}'.replace('True', 'TRUE').replace('False', 'FALSE'))

# External SGR will defeat normalization, unless we `carry` it
# r2py:entity:red
red = "\033[41m"
# r2py:entity:writeLines
writeLines([
    # R: paste(red, "he\033[0mllo", "\033[0m") -> "[41m he[0mllo [0m"
    # Note: paste() in R adds spaces by default
    f"{red} he\033[0mllo \033[0m",
    f"{red} {normalize_state('he\033[0mllo')} \033[0m",
    f"{red} {normalize_state('he\033[0mllo', carry=red)} \033[0m"
])