import numpy as np
import re

# r2py:entity:normalize_state
def normalize_state(x, warn=True, term_cap=None, carry=False):
    """
    Approximates fansi::normalize_state.
    Normalizes ANSI escape sequences by expanding combined codes,
    removing redundancies, and ensuring trailing resets.
    """
    # State tracking
    fg = None # 39
    bg = None # 49
    styles = set()

    def apply_sgr(params_str, cur_fg, cur_bg, cur_styles):
        params = params_str.split(';')
        new_fg, new_bg, new_styles = cur_fg, cur_bg, set(cur_styles)
        for p in params:
            if not p: continue
            try:
                val = int(p)
            except ValueError: continue
            if val == 0:
                new_fg, new_bg, new_styles = None, None, set()
            elif 30 <= val <= 39: new_fg = val
            elif 40 <= val <= 49: new_bg = val
            elif 1 <= val <= 9: new_styles.add(val)
            elif 20 <= val <= 29: new_styles.discard(val - 20)
        return new_fg, new_bg, new_styles

    # Handle carry
    if isinstance(carry, str) and carry:
        carry_matches = re.findall(r'\033\[([0-9;]*m)', carry)
        for m in carry_matches:
            fg, bg, styles = apply_sgr(m[0].rstrip('m'), fg, bg, styles)

    pattern = re.compile(r'(\033\[([0-9;]*m))')
    last_pos = 0
    out = []
    current_fg, current_bg, current_styles = fg, bg, styles

    for match in pattern.finditer(x):
        out.append(x[last_pos:match.start()])
        full_seq = match.group(1)
        params_str = match.group(2).rstrip('m')
        
        current_fg, current_bg, current_styles = apply_sgr(params_str, current_fg, current_bg, current_styles)
        
        if params_str == "0":
            out.append("\033[0m")
        elif params_str == "49":
            pass # unused closing
        elif ";" in params_str:
            # Expand combined SGRs: fg first then bg
            p_vals = [int(p) for p in params_str.split(';') if p]
            style_vals = [v for v in p_vals if 1 <= v <= 29]
            fg_vals = [v for v in p_vals if 30 <= v <= 39]
            bg_vals = [v for v in p_vals if 40 <= v <= 49]
            for v in style_vals: out.append(f"\033[{v}m")
            if fg_vals: out.append(f"\033[{fg_vals[-1]}m")
            if bg_vals: out.append(f"\033[{bg_vals[-1]}m")
        else:
            # Preserve incomplete or single codes
            out.append(full_seq)
        last_pos = match.end()
    
    out.append(x[last_pos:])
    res = "".join(out)

    # Handle trailing resets
    if x.endswith("\033[m") or x.endswith("\033[0m"):
        res = re.sub(r'\033\[(0|m)$', '', res)
        resets = ""
        if current_styles:
            for s in sorted(list(current_styles)):
                if s == 4: resets += "\033[24m"
        if current_fg is not None: resets += "\033[39m"
        if current_bg is not None: resets += "\033[49m"
        res += resets

    return res

# r2py:entity:identical
def identical(x, y):
    return x == y

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        for line in text:
            print(line)
    else:
        print(text, end="")

# --- Execution ---

def r_print(val):
    if isinstance(val, bool):
        print(f'[1] {str(val).upper()}')
    else:
        print(f'[1] "{val}"')

# r2py:entity:normalize_state
r_print(normalize_state("hello\033[42;33m world"))
# r2py:entity:normalize_state_1
r_print(normalize_state("hello\033[42;33m world\033[m"))
# r2py:entity:normalize_state_2
r_print(normalize_state("\033[4mhello\033[42;33m world\033[m"))

# Superflous codes removed
# r2py:entity:normalize_state_3
r_print(normalize_state("\033[31;32mhello\033[m"))
# r2py:entity:normalize_state_4
r_print(normalize_state("\033[31\033[32mhello\033[m"))
# r2py:entity:normalize_state_5
r_print(normalize_state("\033[31mhe\033[49mllo\033[m"))

# Equivalent normalized sequences compare identical
# r2py:entity:identical
r_print(identical(
    normalize_state("\033[31;32mhello\033[m"),
    normalize_state("\033[31mhe\033[49mllo\033[m")
))

# External SGR will defeat normalization, unless we `carry` it
# r2py:entity:red
red = "\033[41m"
# r2py:entity:writeLines
writeLines([
    f"{red} he\033[0mllo \033[0m",
    f"{red} {normalize_state('he\033[0mllo')} \033[0m",
    f"{red} {normalize_state('he\033[0mllo', carry=red)} \033[0m"
])