# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import re

def get_ansi_state(text):
    """Tracks the SGR state of a single string."""
    # SGR pattern: \x1b[ followed by numbers and semicolons, ending in 'm'
    pattern = re.compile(r'\x1b\[([0-9;]*)m')
    fg = None
    bg = None
    
    for match in pattern.finditer(text):
        codes = match.group(1).split(';')
        for code in codes:
            if not code: continue
            val = int(code)
            if val == 0:
                fg = None
                bg = None
            elif val == 39:
                fg = None
            elif val == 49:
                bg = None
            elif 30 <= val <= 37 or 90 <= val <= 97:
                fg = val
            elif 40 <= val <= 47 or 100 <= val <= 107:
                bg = val
    return fg, bg

# r2py:entity:state_at_end
def state_at_end(x, carry=False):
    """
    Equivalent to fansi::state_at_end.
    Returns the state at the end of each element.
    If carry=True, state persists across elements.
    """
    results = []
    current_fg = None
    current_bg = None
    
    for text in x:
        if not carry:
            # Reset state for each element if not carrying
            temp_fg, temp_bg = None, None
            # Calculate state for this string starting from clean
            # Note: R fansi behavior on non-carry is per-element state
            # We simulate the state machine for this string
            pattern = re.compile(r'\x1b\[([0-9;]*)m')
            for match in pattern.finditer(text):
                codes = match.group(1).split(';')
                for code in codes:
                    if not code: continue
                    val = int(code)
                    if val == 0: temp_fg, temp_bg = None, None
                    elif val == 39: temp_fg = None
                    elif val == 49: temp_bg = None
                    elif 30 <= val <= 37 or 90 <= val <= 97: temp_fg = val
                    elif 40 <= val <= 47 or 100 <= val <= 107: temp_bg = val
            
            res_parts = []
            if temp_fg is not None: res_parts.append(f"\x1b[{temp_fg}m")
            if temp_bg is not None: res_parts.append(f"\x1b[{temp_bg}m")
            # R's fansi output for state_at_end usually combines them or returns sequence
            # Based on verification: R produced "\033[44m" "\033[33m"
            # It seems to return the last active SGR sequence.
            # Let's refine to return the combined sequence.
            final_seq = ""
            if temp_fg is not None and temp_bg is not None:
                final_seq = f"\x1b[{temp_fg};{temp_bg}m"
            elif temp_fg is not None:
                final_seq = f"\x1b[{temp_fg}m"
            elif temp_bg is not None:
                final_seq = f"\x1b[{temp_bg}m"
            results.append(final_seq)
            
        else:
            # Carry state across elements
            pattern = re.compile(r'\x1b\[([0-9;]*)m')
            for match in pattern.finditer(text):
                codes = match.group(1).split(';')
                for code in codes:
                    if not code: continue
                    val = int(code)
                    if val == 0: current_fg, current_bg = None, None
                    elif val == 39: current_fg = None
                    elif val == 49: current_bg = None
                    elif 30 <= val <= 37 or 90 <= val <= 97: current_fg = val
                    elif 40 <= val <= 47 or 100 <= val <= 107: current_bg = val
            
            final_seq = ""
            if current_fg is not None and current_bg is not None:
                final_seq = f"\x1b[{current_fg};{current_bg}m"
            elif current_fg is not None:
                final_seq = f"\x1b[{current_fg}m"
            elif current_bg is not None:
                final_seq = f"\x1b[{current_bg}m"
            results.append(final_seq)
            
    return results

# r2py:entity:close
def close_state(states, normalize=True):
    """
    Equivalent to fansi::close_state.
    Converts state sequences into reset sequences.
    """
    results = []
    for s in states:
        if not s:
            results.append("")
            continue
        
        # Extract codes from \x1b[...m
        match = re.search(r'\x1b\[([0-9;]*)m', s)
        if not match:
            results.append("")
            continue
            
        codes = match.group(1).split(';')
        res_parts = []
        for code in codes:
            if not code: continue
            val = int(code)
            if 30 <= val <= 37 or 90 <= val <= 97:
                res_parts.append("\x1b[39m")
            elif 40 <= val <= 47 or 100 <= val <= 107:
                res_parts.append("\x1b[49m")
        
        results.append("".join(res_parts))
    return results

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

# --- Translated Code ---

# r2py:entity:x
x = ["\033[44mhello", "\033[33mworld"]

# state_at_end(x)
# r2py:entity:state_at_end
state_res = state_at_end(x)
print(f'[1] ' + ' '.join(f'"{s}"' for s in state_res))

# state_at_end(x, carry=TRUE)
# r2py:entity:state_at_end_1
state_carry_res = state_at_end(x, carry=True)
print(f'[1] ' + ' '.join(f'"{s}"' for s in state_carry_res))

# (close <- close_state(state_at_end(x, carry=TRUE), normalize=TRUE))
# r2py:entity:close
close = close_state(state_at_end(x, carry=True), normalize=True)
print(f'[1] ' + ' '.join(f'"{s}"' for s in close))

# writeLines(paste0(x, close, " no style"))
# r2py:entity:writeLines
combined = [f"{xi}{ci} no style" for xi, ci in zip(x, close)]
writeLines(combined)