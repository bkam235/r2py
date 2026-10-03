import numpy as np
import pandas as pd
import locale
import sys

def int_to_utf8(ints):
    """Equivalent to R's intToUtf8"""
    return "".join(chr(i) for i in ints)

def output_utf8():
    """Helper to determine if output is UTF-8 capable"""
    try:
        encoding = getattr(sys.stdout, 'encoding', None)
        if encoding and 'utf-8' in encoding.lower():
            return True
        loc = locale.getlocale(locale.LC_CTYPE)
        return loc[1] is not None and 'UTF-8' in loc[1].upper()
    except:
        return False

# r2py:entity:utf8_print
def utf8_print(x, chars=None, quote=True, na_print=None, print_gap=None, 
               right=False, max_val=None, names=None, rownames=None, 
               escapes=None, display=True, style=True, utf8=None):
    """
    Python implementation of the utf8_print logic.
    """
    if x is None:
        return None

    if not isinstance(x, (str, list, np.ndarray, pd.DataFrame, pd.Series)):
        raise TypeError("argument is not a character object")

    # Handle UTF-8 output capability
    use_utf8 = utf8 if utf8 is not None else output_utf8()

    def format_val(val):
        if val is None or (isinstance(val, float) and np.isnan(val)):
            return na_print if na_print else "NA"
        
        s = str(val)
        
        # If not UTF-8, represent non-ASCII as \UXXXXXXXX
        if not use_utf8:
            res = ""
            for char in s:
                if ord(char) > 127:
                    res += f"\\U{ord(char):08x}"
                else:
                    res += char
            s = res
        
        if quote:
            s = f'"{s}"'
        return s

    def apply_style(text, style_code):
        if style and style_code:
            return f"\033[{style_code}m{text}\033[0m"
        return text

    # Convert to array for consistent handling
    if isinstance(x, str):
        data = np.array([x])
        is_scalar = True
    elif isinstance(x, pd.DataFrame):
        data = x.values.astype(object)
        is_scalar = False
    elif isinstance(x, (list, np.ndarray, pd.Series)):
        data = np.array(x, dtype=object)
        is_scalar = False
    else:
        data = np.array([str(x)])
        is_scalar = False

    # Handle 2D (Matrix)
    if data.ndim == 2:
        rows, cols = data.shape
        col_headers = [apply_style(f"[,{i+1}]", names) for i in range(cols)]
        print(" ".join(col_headers))
        for r in range(rows):
            row_header = apply_style(f"[{r+1},]", rownames)
            # R matrices are column-major, but numpy is row-major.
            # The input matrix_data = np.array([...]).reshape(4, 5) in main script 
            # needs to match R's matrix(1:20, 4, 5) which is col-major.
            row_vals = " ".join(format_val(data[r, c]) for c in range(cols))
            print(f"{row_header} {row_vals}")
    else:
        # Handle Vector
        flat_data = data.flatten()
        n = len(flat_data)
        limit = max_val if max_val is not None else 1000
        
        formatted_vals = [format_val(v) for v in flat_data[:limit]]
        line_content = " ".join(formatted_vals)
        full_string = f"[1] {line_content}"
        
        # Truncation logic: R's utf8_print truncates the total output line
        if chars is not None:
            if len(full_string) > chars:
                print(full_string[:chars] + "…")
            else:
                print(full_string)
        else:
            # Default R truncation for utf8_print is typically around 80 chars for long strings
            if len(full_string) > 80:
                print(full_string[:80] + "…")
            else:
                print(full_string)
        
        if n > limit:
            print(f" [ reached getOption(\"max.print\") -- omitted {n - limit} entries ]")

    return x

# --- MAIN SCRIPT ---

# printing (assumes that output is capable of displaying Unicode 10.0.0)
emoji_range = [0x1F600 + i for i in range(80)]
emoji_string = int_to_utf8(emoji_range)

# with default R print function
# r2py:entity:print
print(f'[1] "{emoji_string}"')

# with utf8_print, truncates line
# r2py:entity:utf8_print
utf8_print(emoji_string)

# higher character limit
# r2py:entity:utf8_print_1
utf8_print(emoji_string, chars=1000)

# in C locale, output ASCII (same results on all platforms)
try:
# r2py:entity:oldlocale
    oldlocale = locale.setlocale(locale.LC_CTYPE)
# r2py:entity:invisible
    locale.setlocale(locale.LC_CTYPE, 'C')
# r2py:entity:utf8_print_2
    utf8_print(emoji_string)
# r2py:entity:invisible_1
    locale.setlocale(locale.LC_CTYPE, oldlocale)
except:
    # Fallback to simulate C locale output explicitly
    utf8_print(emoji_string, utf8=False)

# Mac and Linux only: style the names
# R's matrix(1:20, 4, 5) fills column-major.
# To replicate in numpy: create 1:20, reshape to (5, 4) then transpose to (4, 5)
# r2py:entity:utf8_print_3
matrix_data = np.arange(1, 21).reshape(5, 4).T.astype(str)
utf8_print(matrix_data, names="1;4", rownames="2;3")