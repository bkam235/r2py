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

    # Handle Matrix/Array formatting
    if isinstance(x, np.ndarray) and x.ndim == 2:
        rows, cols = x.shape
        header = "      " + " ".join([f"[,{i+1}]" for i in range(cols)])
        print(header)
        for i in range(rows):
            # R matrix: elements are quoted, separated by two spaces
            row_vals = "  ".join([f'"{val}"' for val in x[i]])
            line = f"[{i+1},] {row_vals}"
            if style and rownames:
                print(f"\033[{rownames}m{line}\033[0m")
            else:
                print(line)
        return x

    # Handle Vector/String formatting
    if isinstance(x, str):
        content = x
        # R default truncate for utf8_print is 60 characters
        limit = chars if chars is not None else 60
        
        # Convert non-ASCII to \U000xxxxx
        escaped_chars = []
        for c in content:
            if ord(c) > 127:
                escaped_chars.append(f"\\U{ord(c):08x}")
            else:
                escaped_chars.append(c)
        
        full_escaped = "".join(escaped_chars)
        
        if len(full_escaped) > limit:
            display_text = full_escaped[:limit] + "..."
        else:
            display_text = full_escaped
        
        formatted_val = f'"{display_text}"' if quote else display_text
        output = f"      [1] {formatted_val}"
        
        if style and names:
            print(f"\033[{names}m{output}\033[0m")
        else:
            print(output)
        return x
    
    print(str(x))
    return x

# printing (assumes that output is capable of displaying Unicode 10.0.0)
emoji_str = intToUtf8(np.arange(0x1F600, 0x1F600 + 80))
# R: print(intToUtf8(0x1F600 + 0:79))
# Standard R print(char) prints the actual glyphs if possible
# r2py:entity:print
print(f'[1] "{emoji_str}"')

# R: utf8_print(intToUtf8(0x1F600 + 0:79))
# r2py:entity:utf8_print
utf8_print(emoji_str)

# R: utf8_print(intToUtf8(0x1F600 + 0:79), chars = 1000)
# r2py:entity:utf8_print_1
utf8_print(emoji_str, chars=1000)

# in C locale, output ASCII (same results on all platforms)
# r2py:entity:oldlocale
oldlocale = locale.getlocale(locale.LC_CTYPE)
try:
# r2py:entity:invisible
    locale.setlocale(locale.LC_CTYPE, "C") # switch to C locale
# r2py:entity:utf8_print_2
    utf8_print(emoji_str)
finally:
    # Reverting to original locale
# r2py:entity:invisible_1
    loc = oldlocale[0] if isinstance(oldlocale, tuple) else oldlocale
    if loc:
        locale.setlocale(locale.LC_CTYPE, loc)

# Mac and Linux only: style the names
# R: utf8_print(matrix(as.character(1:20), 4, 5), names = "1;4", rownames = "2;3")
# r2py:entity:utf8_print_3
mat_data = np.arange(1, 21).astype(str).reshape(4, 5, order='F')
utf8_print(mat_data, names="1;4", rownames="2;3")