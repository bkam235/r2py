import numpy as np
import locale
import sys

def intToUtf8(ints):
    return "".join(chr(i) for i in ints)

# r2py:entity:utf8_print
def utf8_print(x, chars=None, quote=True, na_print=None, print_gap=None, 
               right=False, max_val=None, names=None, rownames=None, 
               escapes=None, display=True, style=True, utf8=None):
    if x is None:
        return None
    
    if not isinstance(x, (str, list, tuple, np.ndarray)):
        raise TypeError("argument is not a character object")

    # Helper to simulate R's character printing (e.g., \U0001f600)
    def r_format_char_vec(val):
        if isinstance(val, str):
            # R's utf8_print often represents non-ASCII as \UXXXXXXXX in certain outputs
            return "".join(f"\\U{ord(c):08x}" if ord(c) > 0xFFFF else chr(ord(c)) for c in val)
        return str(val)

    # Handle matrix case
    if isinstance(x, np.ndarray) and x.ndim == 2:
        rows, cols = x.shape
        header = " ".join([f"[,{i+1}]" for i in range(cols)])
        print(f"      {header}")
        for i in range(rows):
            row_label = f"[{i+1},]"
            row_vals = " ".join([f'"{val}"' for val in x[i]])
            print(f"{row_label} {row_vals}")
        return x

    # Handle vector/string case
    if isinstance(x, str):
        data = x
    elif isinstance(x, (list, tuple, np.ndarray)):
        data = "".join(map(str, x)) if isinstance(x, np.ndarray) and x.ndim == 1 else "".join(x)
    else:
        data = str(x)

    formatted = r_format_char_vec(data)
    
    # R's utf8_print truncates based on the 'chars' argument
    if chars is not None and len(formatted) > chars:
        formatted = formatted[:chars] + "…"
    elif chars is None and len(formatted) > 70: # Default R truncation for long strings in print
        formatted = formatted[:70] + "…"
    
    # R's print style for characters: [1] "..."
    print(f'      [1] "{formatted}"')
    return x

# printing (assumes that output is capable of displaying Unicode 10.0.0)
emojis_list = [0x1F600 + i for i in range(80)]
emojis_str = intToUtf8(emojis_list)

# R's print(intToUtf8(...)) outputs the actual emojis if the terminal supports it
# r2py:entity:print
print(f'[1] "{emojis_str}"')

# r2py:entity:utf8_print
utf8_print(emojis_str)

# r2py:entity:utf8_print_1
utf8_print(emojis_str, chars=1000)

# in C locale, output ASCII (same results on all platforms)
try:
    # r2py:entity:oldlocale
# r2py:entity:oldlocale
    oldlocale = locale.getlocale(locale.LC_CTYPE)
    # r2py:entity:invisible
# r2py:entity:invisible
    locale.setlocale(locale.LC_CTYPE, 'C') 
    # r2py:entity:utf8_print_2
# r2py:entity:utf8_print_2
    utf8_print(emojis_str)
    # r2py:entity:invisible_1
# r2py:entity:invisible_1
    locale.setlocale(locale.LC_CTYPE, oldlocale)
except (locale.Error, ValueError):
    # Fallback if 'C' locale is not available
    utf8_print(emojis_str)

# Mac and Linux only: style the names
# matrix(as.character(1:20), 4, 5) fills column-wise in R
# r2py:entity:utf8_print_3
matrix_data = np.arange(1, 21).reshape(5, 4).T.astype(str)
utf8_print(matrix_data, names="1;4", rownames="2;3")