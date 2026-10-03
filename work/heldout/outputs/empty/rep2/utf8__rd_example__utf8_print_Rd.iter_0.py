# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np

# Helper function to mimic R's intToUtf8
# r2py:entity:print
def int_to_utf8(start, length):
    return "".join(chr(i) for i in range(start, start + length))

# Helper function to mimic utf8_print
# r2py:entity:utf8_print
def utf8_print(data, chars=None):
    if isinstance(data, str):
        output = data
        if chars is not None:
            output = data[:chars]
        else:
            # Default R utf8_print behavior truncates long lines
            # approximating with a reasonable default limit (e.g., 80)
            output = data[:80]
        print(output)
    elif isinstance(data, (pd.DataFrame, np.ndarray)):
        print(data)
    else:
        print(data)

# print(intToUtf8(0x1F600 + 0:79))
# r2py:entity:print
print(int_to_utf8(0x1F600, 80))

# utf8_print(intToUtf8(0x1F600 + 0:79))
# r2py:entity:utf8_print
utf8_print(int_to_utf8(0x1F600, 80))

# utf8_print(intToUtf8(0x1F600 + 0:79), chars = 1000)
# r2py:entity:utf8_print_1
utf8_print(int_to_utf8(0x1F600, 80), chars=1000)

# Locale switching is handled differently in Python; 
# locale.setlocale is the equivalent, but typically not needed for UTF-8 in Python 3.
import locale
# r2py:entity:oldlocale
oldlocale = locale.getlocale(locale.LC_CTYPE)
try:
# r2py:entity:invisible
    locale.setlocale(locale.LC_CTYPE, 'C')
# r2py:entity:utf8_print_2
    utf8_print(int_to_utf8(0x1F600, 80))
finally:
# r2py:entity:invisible_1
    locale.setlocale(locale.LC_CTYPE, oldlocale)

# utf8_print(matrix(as.character(1:20), 4, 5), names = "1;4", rownames = "2;3")
# r2py:entity:utf8_print_3
m_data = np.arange(1, 21).astype(str).reshape(4, 5)
d = pd.DataFrame(m_data, 
                 columns=[str(i) for i in range(1, 5)], 
                 index=[str(i) for i in range(2, 6)]) # approximating "2;3" relative indexing
utf8_print(d)