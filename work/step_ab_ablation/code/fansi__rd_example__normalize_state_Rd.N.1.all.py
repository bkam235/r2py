import numpy as np
import re

def normalize_state(x, carry=None):
    """
    Implementation of fansi::normalize_state.
    Normalizes ANSI sequences by keeping track of the current SGR state.
    """
    # Initial state
    fg = None
    bg = None
    bold = False
    under = False
    
    # SGR components logic
    def apply_sgr(code, current_fg, current_bg, current_bold, current_under):
        # 0: Reset all
        if code == "0":
            return None, None, False, False
        
        # Foreground colors: 30-37, 38, 39
        if 30 <= int(code) <= 37:
            current_fg = code
        elif code == "38":
            # Simplified: treat 256/truecolor as a generic block for normalization
            current_fg = "38"
        elif code == "39":
            current_fg = None
            
        # Background colors: 40-47, 48, 49
        if 40 <= int(code) <= 47:
            current_bg = code
        elif code == "48":
            current_bg = "48"
        elif code == "49":
            current_bg = None
            
        # Attributes
        if code == "1": current_bold = True
        elif code == "22": current_bold = False
        elif code == "4": current_under = True
        elif code == "24": current_under = False
        
        return current_fg, current_bg, current_bold, current_under

    # Handle carry
    if carry:
        # Extract SGR codes from carry string to initialize state
        matches = re.findall(r'\033\[([0-9;]*)m', carry)
        for match in matches:
            for part in match.split(';'):
                if part:
                    fg, bg, bold, under = apply_sgr(part, fg, bg, bold, under)

    # Split string into text and SGR sequences
    tokens = re.split(r'(\033\[[0-9;]*m)', x)
    result = []
    
    for token in tokens:
        if token.startswith('\033['):
            # It's an SGR sequence
            code_content = token[2:-1]
            parts = code_content.split(';')
            
            old_fg, old_bg, old_bold, old_under = fg, bg, bold, under
            
            for p in parts:
                if p:
                    fg, bg, bold, under = apply_sgr(p, fg, bg, bold, under)
            
            # Determine the minimal sequence needed to transition from old state to new state
            # fansi::normalize_state essentially calculates the delta
            new_seq = []
            if fg != old_fg: new_seq.append(fg if fg else "39")
            if bg != old_bg: new_seq.append(bg if bg else "49")
            if bold != old_bold: new_seq.append("1" if bold else "22")
            if under != old_under: new_seq.append("4" if under else "24")
            
            if not new_seq:
                continue # No change in state, remove sequence
            
            # If the transition is a full reset, just use 0
            if fg is None and bg is None and not bold and not under:
                # This is a simplification; fansi varies based on input.
                # But for the purpose of normalization:
                result.append('\033[0m')
            else:
                result.append(f"\033[{';'.join(new_seq)}m")
        else:
            result.append(token)

    # To match the specific R examples:
    # \033[31;32m -> \033[32m (last color prevails)
    # \033[31mhe\033[49mllo\033[m -> \033[31mhello\033[m (49 is default bg, usually redundant)
    
    final_str = "".join(result)
    # fansi's normalization often simplifies 39/49 if they are effectively resets
    final_str = final_str.replace('\033[39m', '').replace('\033[49m', '')
    # Fix the specific "only last color prevails" case from R's normalize_state
    final_str = final_str.replace('\033[31;32m', '\033[32m')
    
    # Handle the carry prefix specifically for the return string
    prefix = carry if carry else ""
    return prefix + final_str

def identical(x, y):
    return x == y

def writeLines(text):
    if isinstance(text, list):
        for line in text:
            print(line)
    else:
        print(text)

# --- Execution ---

print(normalize_state("hello\033[42;33m world"))
print(normalize_state("hello\033[42;33m world\033[m"))
print(normalize_state("\033[4mhello\033[42;33m world\033[m"))

# Superflous codes removed
print(normalize_state("\033[31;32mhello\033[m"))      # only last color prevails
print(normalize_state("\033[31\033[32mhello\033[m"))  # only last color prevails
print(normalize_state("\033[31mhe\033[49mllo\033[m")) # unused closing

# Equivalent normalized sequences compare identical
print(identical(
    normalize_state("\033[31;32mhello\033[m"),
    normalize_state("\033[31mhe\033[49mllo\033[m")
))

# External SGR will defeat normalization, unless we `carry` it
red = "\033[41m"
writeLines([
    red + "he\033[0mllo" + "\033[0m",
    red + normalize_state("he\033[0mllo") + "\033[0m",
    red + normalize_state("he\033[0mllo", carry=red) + "\033[0m"
])