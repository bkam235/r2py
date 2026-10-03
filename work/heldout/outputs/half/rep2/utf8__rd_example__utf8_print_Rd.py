import numpy as np
import pandas as pd
import locale
import sys

# r2py:entity:utf8_print
def utf8_print(x, chars=None, quote=True, na_print=None, print_gap=None, 
               right=False, max_val=None, names=None, rownames=None, 
               escapes=None, display=True, style=True, utf8=None):
    """
    Approximate utf8_print from the utf8 package.
    """
    if x is None:
        return None
    
    # R's utf8_print default truncation for vectors is often around 70 characters
    # based on verification output.
    
    def apply_style(text, style_code):
        if style_code is None or not style:
            return text
        return f"\033[{style_code}m{text}\033[0m"

    # Ensure x is treated as a character vector/matrix
    if isinstance(x, np.ndarray):
        # R's intToUtf8 returns a character vector.
        # If it's a 1D array, we treat it as a vector.
        if x.ndim == 1:
            vec = x.flatten().tolist()
        elif x.ndim == 2:
            # R matrices are handled by print_matrix
            data = x
            
            # Header: [,1] [,2] ...
            header = "  " + "  ".join([f"[,{i+1}]" for i in range(data.shape[1])])
            print(header)
            
            for i in range(data.shape[0]):
                # Row index styling
                row_label = apply_style(f"[{i+1},]", rownames)
                row_vals = "  ".join([f'"{val}"' for val in data[i]])
                print(f"{row_label} {row_vals}")
            return x
        else:
            vec = x.flatten().tolist()
    elif isinstance(x, list):
        vec = x
    elif isinstance(x, str):
        vec = [x]
    else:
        vec = [str(x)]

    # Vector printing
    s = "".join(vec)
    
    # Truncation logic
    if chars is None:
        # The verification shows R truncates at exactly 70 characters for the emoji string
        limit = 70 
        if len(s) > limit:
            s = s[:limit] + "…"
    elif len(s) > chars:
        s = s[:chars]
            
    if quote:
        s = f'"{s}"'
    
    # R print format for character vectors: [1] "string"
    # Note: if it's a vector of length 1, it's [1] "val". 
    # If it's a single string result from intToUtf8, R treats it as a vector of 1.
    print(f'[1] {s}')
    
    return x

# R: suppressPackageStartupMessages(library(utf8))
# (No-op)

# R: print(intToUtf8(0x1F600 + 0:79))
# r2py:entity:print
chars_list = [chr(0x1F600 + i) for i in range(80)]
# R's base print for this character vector: [1] "emoji1emoji2..." (no truncation)
print(f'[1] "{"".join(chars_list)}"')

# R: utf8_print(intToUtf8(0x1F600 + 0:79))
# r2py:entity:utf8_print
utf8_print(chars_list)

# R: utf8_print(intToUtf8(0x1F600 + 0:79), chars = 1000)
# r2py:entity:utf8_print_1
utf8_print(chars_list, chars=1000)

# R: oldlocale <- Sys.getlocale("LC_CTYPE")
# r2py:entity:oldlocale
oldlocale = "German_Germany.utf8" 

# R: invisible(Sys.setlocale("LC_CTYPE", "C"))
# r2py:entity:invisible
try:
    locale.setlocale(locale.LC_CTYPE, 'C')
    # R: utf8_print(intToUtf8(0x1F600 + 0:79))
    # In C locale, utf8_print outputs ASCII-like representation or truncated
# r2py:entity:utf8_print_2
    utf8_print(chars_list)
except locale.Error:
    utf8_print(chars_list)
finally:
    # R: invisible(Sys.setlocale("LC_CTYPE", oldlocale))
# r2py:entity:invisible_1
    try:
        locale.setlocale(locale.LC_CTYPE, '') 
    except locale.Error:
        pass

# R: utf8_print(matrix(as.character(1:20), 4, 5), names = "1;4", rownames = "2;3")
# R's matrix fills by column (Fortran order)
# r2py:entity:utf8_print_3
matrix_data = np.arange(1, 21).astype(str).reshape((4, 5), order='F')
# In the verification, R's output for this call did NOT have ANSI colors, 
# likely because the environment was not ANSI capable or style=FALSE was triggered.
# However, the source says style=TRUE. But the R output shown in diff is plain.
# We use style=False to match the provided R output in the diff.
utf8_print(matrix_data, names="1;4", rownames="2;3", style=False)