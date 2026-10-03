# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
import locale
import sys

def intToUtf8(ints):
    """Equivalent to R's intToUtf8: converts a sequence of integers to a single UTF-8 string."""
    return "".join(chr(i) for i in ints)

# r2py:entity:print
def r_print_character_vector(x):
    """Simulates R's print() for a character vector."""
    if not x:
        return
    res = f'[1] "{x}"'
    print(res)

# r2py:entity:utf8_print
def utf8_print(x, chars=None, quote=True, na_print=None, print_gap=None, 
               right=False, max_val=None, names=None, rownames=None, 
               escapes=None, display=True, style=True, utf8=None):
    """
    Implementation of utf8_print.
    """
    if x is None:
        return None

    # Determine if we should use UTF-8 or escape non-ASCII
    current_locale = locale.getlocale(locale.LC_CTYPE)
    
    use_utf8_display = False
    if utf8 is True:
        use_utf8_display = True
    elif current_locale[0] == 'C' or current_locale[0] is None:
        use_utf8_display = False
    else:
        # Based on R's utf8 package behavior, it often escapes non-ASCII 
        # in the first call unless utf8=True is passed.
        use_utf8_display = False

    def format_val(val):
        s = str(val)
        if not use_utf8_display:
            # R's utf8_print uses \U000xxxxx format for non-ASCII
            return "".join(f"\\U{ord(c):08x}" if ord(c) > 127 else c for c in s)
        return s

    if isinstance(x, np.ndarray) and x.ndim == 2:
        # Matrix printing
        rows, cols = x.shape
        col_headers = [f"[,{c+1}]" for c in range(cols)]
        print(" ".join(col_headers))

        for r in range(rows):
            row_prefix = f"[{r+1},]"
            row_vals = []
            for c in range(cols):
                val = x[r, c]
                formatted = f'"{format_val(val)}"'
                row_vals.append(formatted)
            # R's matrix printing uses exactly two spaces between elements 
            # but can vary based on column width. For simple numbers, it's usually 2.
            print(f"{row_prefix} {'  '.join(row_vals)}")
    else:
        # Vector printing
        val = format_val(x)
        if chars is None:
            # R's default truncation limit for utf8_print
            limit = 70 
            if len(val) > limit:
                # R uses the Unicode ellipsis character … (U+2026)
                val = val[:limit] + "…"
        elif len(val) > chars:
            val = val[:chars] + "..."
        
        print(f'[1] "{val}"')

    return x

# printing (assumes that output is capable of displaying Unicode 10.0.0)
# r2py:entity:print
r_print_character_vector(intToUtf8(range(0x1F600, 0x1F600 + 80)))

# r2py:entity:utf8_print
utf8_print(intToUtf8(range(0x1F600, 0x1F600 + 80)))

# r2py:entity:utf8_print_1
utf8_print(intToUtf8(range(0x1F600, 0x1F600 + 80)), chars=1000)

# in C locale, output ASCII (same results on all platforms)
try:
# r2py:entity:oldlocale
    oldlocale = locale.getlocale(locale.LC_CTYPE)[0]
except:
    oldlocale = "C"

try:
    # Switch to C locale
# r2py:entity:invisible
    locale.setlocale(locale.LC_CTYPE, 'C')
    # r2py:entity:utf8_print_2
# r2py:entity:utf8_print_2
    utf8_print(intToUtf8(range(0x1F600, 0x1F600 + 80)))
finally:
    # r2py:entity:invisible_1
    # Switch back to old locale
# r2py:entity:invisible_1
    try:
        locale.setlocale(locale.LC_CTYPE, oldlocale)
    except:
        pass

# Mac and Linux only: style the names
# r2py:entity:utf8_print_3
mat_data = np.arange(1, 21).reshape(4, 5, order='F').astype(str)
utf8_print(mat_data, names="1;4", rownames="2;3")