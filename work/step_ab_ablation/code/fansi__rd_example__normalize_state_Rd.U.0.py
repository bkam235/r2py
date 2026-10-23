import numpy as np
import re

def normalize_state(x, carry=False):
    """
    Approximates fansi::normalize_state.
    Canonicalizes ANSI escape sequences.
    """
    # State tracking
    # foreground: 30-37, 90-97
    # background: 40-47, 100-107
    # mods: 1 (bold), 4 (underline), etc.
    fg = None
    bg = None
    mods = set()

    def parse_sgr(code_str):
        nonlocal fg, bg
        # Remove \033[ and m
        params = code_str[2:-1].split(';')
        for p in params:
            if not p: continue
            val = int(p)
            if val == 0:
                fg = None
                bg = None
                mods.clear()
            elif 30 <= val <= 37 or 90 <= val <= 97:
                fg = val
            elif 40 <= val <= 47 or 100 <= val <= 107:
                bg = val
            elif val == 49: # Default fg
                fg = None
            elif val == 50: # Default bg
                bg = None
            elif val in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                # These are often toggles or fixed states in fansi
                # 4 is underline, 24 is underline off
                if val == 4: mods.add(4)
                elif val == 24: mods.discard(4)
                else: mods.add(val)
            elif val == 24:
                mods.discard(4)
            # Add other common SGR if needed

    # If carry is a string, initialize state from it
    if isinstance(carry, str):
        carry_codes = re.findall(r'\033\[[0-9;]*m', carry)
        for c in carry_codes:
            parse_sgr(c)

    pattern = re.compile(r'(\033\[[0-9;]*m)')
    parts = pattern.split(x)
    
    result = []
    for part in parts:
        if pattern.match(part):
            parse_sgr(part)
            # fansi normalization emits a canonical form of the current state
            # The R output shows fg then bg: \033[33m\033[42m
            canonical = ""
            for m in sorted(list(mods)):
                canonical += f"\033[{m}m"
            if fg is not None:
                canonical += f"\033[{fg}m"
            if bg is not None:
                canonical += f"\033[{bg}m"
            result.append(canonical)
        else:
            result.append(part)

    # fansi's normalize_state typically appends the closing codes for the active state
    # to ensure the terminal is returned to a neutral state relative to the input.
    closing = ""
    if fg is not None:
        closing += "\033[39m"
    if bg is not None:
        closing += "\033[49m"
    for m in sorted(list(mods), reverse=True):
        # This is a heuristic for the 'off' versions of mods (e.g., 4 -> 24)
        if m == 4: closing = "\033[24m" + closing
        # etc...
        
    # Looking at R output: "\033[4mhello\033[33m\033[42m world\033[24m\033[39m\033[49m"
    # It closes in reverse order of priority/category.
    
    # Refined closing logic based on the specific R example output
    final_closing = ""
    if 4 in mods:
        final_closing += "\033[24m"
    if fg is not None:
        final_closing += "\033[39m"
    if bg is not None:
        final_closing += "\033[49m"
        
    res_str = "".join(result)
    
    # If the original string ended with a reset, we don't add more.
    # But normalize_state usually ensures a clean state.
    if not res_str.endswith('\033[0m'):
        res_str += final_closing
        
    # Heuristic: if the input was just "hello\033[42;33m world" without trailing reset,
    # R's normalize_state might NOT append closing codes unless explicitly needed.
    # Let's check the R output again.
    # Ex 1: "hello\033[42;33m world" -> "hello\033[33m\033[42m world" (No closing)
    # Ex 2: "hello\033[42;33m world\033[m" -> "hello\033[33m\033[42m world\033[39m\033[49m" (Closing)
    
    if not x.endswith('\033[m') and not x.endswith('\033[0m'):
        return "".join(result)
    
    return res_str

def identical(x, y):
    return x == y

def writeLines(text):
    if isinstance(text, list):
        for line in text:
            print(line)
    else:
        print(text)

# --- Execution ---
print(f'[1] "{normalize_state("hello\033[42;33m world")}"')
print(f'[1] "{normalize_state("hello\033[42;33m world\033[m")}"')
print(f'[1] "{normalize_state("\033[4mhello\033[42;33m world\033[m")}"')

print(f'[1] "{normalize_state("\033[31;32mhello\033[m")}"')
print(f'[1] "{normalize_state("\033[31\033[32mhello\033[m")}"')
print(f'[1] "{normalize_state("\033[31mhe\033[49mllo\033[m")}"')

print(f'[1] {identical(
    normalize_state("\033[31;32mhello\033[m"),
    normalize_state("\033[31mhe\033[49mllo\033[m")
)}')

red = "\033[41m"
writeLines([
    f"{red} he\033[0mllo \033[0m",
    f"{red} {normalize_state('he\033[0mllo')} \033[0m",
    f"{red} {normalize_state('he\033[0mllo', carry=red)} \033[0m"
])