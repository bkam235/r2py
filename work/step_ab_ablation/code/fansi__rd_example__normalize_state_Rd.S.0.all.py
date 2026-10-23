import numpy as np
import re

# r2py:entity:normalize_state
def normalize_state(x, carry=None):
    """
    Approximates fansi::normalize_state.
    Normalizes ANSI escape sequences by removing redundant or superfluous codes.
    """
    # State tracks current SGR values: { 'fg': val, 'bg': val, 'others': set() }
    state = {'fg': None, 'bg': None, 'others': set()}
    
    def apply_sgr(sgr_str, current_state):
        # SGR codes are in the format \033[...m
        # Extract the numeric parts
        match = re.search(r'\[(.*)m', sgr_str)
        if not match:
            return current_state
        
        params = match.group(1).split(';')
        for p in params:
            if not p: continue
            val = int(p)
            if val == 0: # Reset all
                current_state['fg'] = None
                current_state['bg'] = None
                current_state['others'] = set()
            elif val == 39: # Default fg
                current_state['fg'] = None
            elif val == 49: # Default bg
                current_state['bg'] = None
            elif 30 <= val <= 37 or 90 <= val <= 97: # Foreground
                current_state['fg'] = val
            elif 40 <= val <= 47 or 100 <= val <= 107: # Background
                current_state['bg'] = val
            elif val == 1: # Bold
                current_state['others'].add(1)
            elif val == 4: # Underline
                current_state['others'].add(4)
            # ... other SGRs can be added here if needed
        return current_state

    def state_to_sgr(current_state):
        # Convert current state back to a minimal SGR sequence
        codes = []
        # If everything is reset, \033[0m is common, but fansi normalization
        # often produces the minimal necessary sequence.
        if current_state['fg'] is not None:
            codes.append(str(current_state['fg']))
        if current_state['bg'] is not None:
            codes.append(str(current_state['bg']))
        for o in sorted(list(current_state['others'])):
            codes.append(str(o))
        
        if not codes:
            return "" # Or \033[0m depending on exact fansi behavior
        return f"\033[{';'.join(codes)}m"

    # Initialize state if carry is provided
    if carry:
        apply_sgr(carry, state)

    # Process string
    result = []
    last_pos = 0
    # Find all SGR sequences
    for match in re.finditer(r'\033\[[0-9;]*m', x):
        # Add text before the sequence
        result.append(x[last_pos:match.start()])
        
        # Update state
        sgr_seq = match.group(0)
        state = apply_sgr(sgr_seq, state)
        
        # The "normalization" in fansi effectively recalculates the 
        # necessary sequence to reach the current state from the previous one,
        # or simply outputs the current state if it changed.
        # For these examples, replacing the sequence with the normalized version:
        result.append(state_to_sgr(state))
        last_pos = match.end()
        
    result.append(x[last_pos:])
    
    final_str = "".join(result)
    
    # Final cleanup to match specific R output quirks:
    # fansi often preserves the trailing \033[0m if it was in the original
    # but removes redundant internal ones.
    return (carry if carry else "") + final_str if carry else final_str

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
print(normalize_state("hello\033[42;33m world"))
# r2py:entity:normalize_state_1
print(normalize_state("hello\033[42;33m world\033[m"))
# r2py:entity:normalize_state_2
print(normalize_state("\033[4mhello\033[42;33m world\033[m"))

# Superflous codes removed
# r2py:entity:normalize_state_3
print(normalize_state("\033[31;32mhello\033[m"))      # only last color prevails
# r2py:entity:normalize_state_4
print(normalize_state("\033[31\033[32mhello\033[m"))  # only last color prevails
# r2py:entity:normalize_state_5
print(normalize_state("\033[31mhe\033[49mllo\033[m")) # unused closing

# Equivalent normalized sequences compare identical
# r2py:entity:identical
print(identical(
    normalize_state("\033[31;32mhello\033[m"),
    normalize_state("\033[31mhe\033[49mllo\033[m")
))

# External SGR will defeat normalization, unless we `carry` it
# r2py:entity:red
red = "\033[41m"
# r2py:entity:writeLines
writeLines([
    red + "he\033[0mllo" + "\033[0m",
    red + normalize_state("he\033[0mllo") + "\033[0m",
    red + normalize_state("he\033[0mllo", carry=red) + "\033[0m"
])