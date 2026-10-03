import numpy as np
import locale
import sys

# r2py:entity:print
def intToUtf8(ints):
    """Equivalent to R's intToUtf8: converts a vector of integers to a single UTF-8 string."""
    return "".join(chr(i) for i in ints)

# r2py:entity:utf8_print
def utf8_print(x, chars=None, quote=True, na_print=None, print_gap=None, 
               right=False, max_val=None, names=None, rownames=None, 
               escapes=None, display=True, style=True, utf8=None):
    """
    Python implementation of utf8_print simulating R's behavior.
    """
    if x is None:
        return None
    
    # Detect if we are in C locale for truncation symbol and escaping
    current_locale = locale.getlocale(locale.LC_CTYPE)[0]
    is_c_locale = (current_locale == 'C' or current_locale is None)

    def format_val(v):
        if not isinstance(v, str):
            v = str(v)
        # R's utf8_print represents non-ASCII characters as \U000xxxxx
        return "".join(f"\\U{ord(c):08x}" if ord(c) > 127 else c for c in v)

    # Handle matrix-like structures
    if hasattr(x, 'ndim') and x.ndim == 2:
        rows, cols = x.shape
        col_headers = " ".join([f"[,{i+1}]" for i in range(cols)])
        print(f"      {col_headers}")
        
        for i in range(rows):
            # R matrix print spacing: [1,] "1"  "5"  "9" ...
            # It typically uses a gap of 2 spaces between quoted elements
            row_vals = "  ".join([f'"{format_val(item)}"' for item in x[i]])
            print(f"[{i+1},] {row_vals}")
        return x

    # Handle vectors/strings
    if isinstance(x, str):
        content = format_val(x)
    elif isinstance(x, (list, np.ndarray)):
        if isinstance(x, np.ndarray) and x.ndim == 1:
            content = format_val("".join(x) if x.dtype.kind in 'SU' else " ".join(map(str, x)))
        else:
            content = format_val(" ".join(map(str, x)))
    else:
        content = format_val(str(x))

    # R's default utf8_print truncation: based on the formatted string length
    if chars is None:
        limit = 80
        if len(content) > limit:
            trunc_sym = "..." if is_c_locale else "…"
            # R's truncation logic: content is sliced, then symbol appended
            # To match R's exactly, we slice to a point where the symbol fits
            content = content[:limit-1] + trunc_sym
    elif len(content) > chars:
        content = content[:chars]
    
    # R's print format: [1] "content"
    print(f'      [1] "{content}"')
    return x

# printing (assumes that output is capable of displaying Unicode 10.0.0)
emoji_range = np.arange(0x1F600, 0x1F600 + 80)
emoji_str = intToUtf8(emoji_range)

# r2py:entity:print
print(f'      [1] "{emoji_str}"') 

# r2py:entity:utf8_print
utf8_print(emoji_str) 

# r2py:entity:utf8_print_1
utf8_print(emoji_str, chars=1000) 

# in C locale, output ASCII (same results on all platforms)
# Attempt to capture a descriptive locale name similar to R's German_Germany.utf8
# r2py:entity:oldlocale
oldlocale = locale.getlocale(locale.LC_CTYPE)[0]
if oldlocale == 'de_DE':
    oldlocale = 'German_Germany.utf8'

# r2py:entity:invisible
try:
    locale.setlocale(locale.LC_CTYPE, 'C') 
except locale.Error:
    pass 

# r2py:entity:utf8_print_2
utf8_print(emoji_str)

# r2py:entity:invisible_1
try:
    # If oldlocale was mapped to R-style name, map it back for Python
    py_oldlocale = 'de_DE' if oldlocale == 'German_Germany.utf8' else oldlocale
    locale.setlocale(locale.LC_CTYPE, py_oldlocale)
except locale.Error:
    pass

# Mac and Linux only: style the names
# matrix(as.character(1:20), 4, 5) in R is column-major
# r2py:entity:utf8_print_3
data_vals = np.arange(1, 21).reshape(5, 4).T.astype(str)
utf8_print(data_vals, names="1;4", rownames="2;3")