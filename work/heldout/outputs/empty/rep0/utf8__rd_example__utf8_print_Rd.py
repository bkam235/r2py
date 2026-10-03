import numpy as np
import pandas as pd
import locale
import sys

# r2py:entity:print
def intToUtf8(ints):
    """Equivalent to R's intToUtf8: converts integers to a UTF-8 string."""
    return "".join(chr(i) for i in ints)

# r2py:entity:utf8_print
def utf8_print(x, chars=None, quote=True, na_print=None, print_gap=None, 
               right=False, max_val=None, names=None, rownames=None, 
               escapes=None, display=True, style=True, utf8=None):
    """
    Python implementation of R's utf8_print.
    """
    if x is None:
        return None

    # Validate input
    if isinstance(x, str):
        x_vec = np.array([x], dtype=object)
    elif isinstance(x, (list, np.ndarray, pd.Series)):
        x_vec = np.array(x, dtype=object)
    elif isinstance(x, pd.DataFrame):
        x_vec = x.values
    else:
        # R's stop("argument is not a character object")
        raise TypeError("argument is not a character object")

    # Determine if we should use escaped Unicode representation
    # R's utf8_print uses \U escapes in C locale
    use_escapes = False
    try:
        curr_locale = locale.getlocale(locale.LC_CTYPE)
        if curr_locale[0] == 'C':
            use_escapes = True
    except:
        pass
    
    def format_val(val):
        s = str(val)
        # R's utf8_print uses \U escapes for non-ASCII if use_escapes is True 
        # OR if it is truncating characters.
        if use_escapes or (chars is not None):
            res = ""
            for char in s:
                if ord(char) > 127:
                    res += f"\\U{ord(char):08x}"
                else:
                    res += char
            return res
        return s

    def apply_style(val, style_code):
        if style_code is None or not style: return val
        return f"\033[{style_code}m{val}\033[0m"

    if len(np.shape(x_vec)) == 2:
        rows, cols = x_vec.shape
        header = "      " + " ".join([f"[,{i+1}]" for i in range(cols)])
        print(header)
        for i in range(rows):
            row_label = f"[{i+1},]"
            row_label = apply_style(row_label, rownames)
            row_vals = []
            for j in range(cols):
                val = format_val(x_vec[i, j])
                row_vals.append(f'"{val}"' if quote else val)
            print(f"{row_label} {'  '.join(row_vals)}")
        return x

    else:
        flat_x = x_vec.flatten()
        formatted_vals = []
        for v in flat_x:
            fv = format_val(v)
            if chars is not None and len(fv) > chars:
                # R's utf8_print truncation logic
                fv = fv[:chars] + "…"
            formatted_vals.append(f'"{fv}"' if quote else fv)
        
        out = " ".join(formatted_vals)
        print(f"[1] {out}")
        return x

# --- Main Execution ---

# printing (assumes that output is capable of displaying Unicode 10.0.0)
emoji_range = range(0x1F600, 0x1F600 + 80)
emoji_str = intToUtf8(emoji_range)

# with default R print function
# r2py:entity:print
print(f'[1] "{emoji_str}"')

# with utf8_print, truncates line
# r2py:entity:utf8_print
utf8_print(emoji_str, chars=20)

# higher character limit
# r2py:entity:utf8_print_1
utf8_print(emoji_str, chars=1000)

# in C locale, output ASCII
# r2py:entity:oldlocale
old_locale = locale.getlocale(locale.LC_CTYPE)
# r2py:entity:invisible
try:
    locale.setlocale(locale.LC_CTYPE, 'C')
# r2py:entity:utf8_print_2
    # r2py:entity:utf8_print_2
    utf8_print(emoji_str)
except locale.Error:
    # Fallback if 'C' is not available on this OS
    utf8_print(emoji_str)
# r2py:entity:invisible_1
try:
    locale.setlocale(locale.LC_CTYPE, old_locale if old_locale[0] else 'en_US.UTF-8')
except locale.Error:
    pass

# Mac and Linux only: style the names
# matrix(as.character(1:20), 4, 5)
# r2py:entity:utf8_print_3
data_array = np.arange(1, 21).reshape(5, 4).T.astype(str) 
utf8_print(data_array, names="1;4", rownames="2;3")