# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import numpy as np
import pandas as pd
import unicodedata

def stri_trans_nfkd(text):
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return text
    return unicodedata.normalize('NFKD', text)

# r2py:entity:stri_duplicated
def stri_duplicated(str_vec, from_last=False, strength=None):
    # Handle strings with potential Unicode normalization or case insensitivity
    # strength=1 in stringi usually means primary level (case/accent insensitive)
    processed = []
    for x in str_vec:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            processed.append(None)
        else:
            val = str(x)
            if strength == 1:
                val = unicodedata.normalize('NFKD', val).casefold()
            processed.append(val)

    n = len(processed)
    duplicated = [False] * n
    seen = set()
    
    if not from_last:
        for i in range(n):
            val = processed[i]
            # In R, NA is treated as a value for duplication checks in stri_duplicated
            # We use a sentinel for None to track it in the set
            marker = f"__NA_{i}" if val is None else val
            # Actually, R's stri_duplicated treats NAs as identical
            marker = "STR_NA_SENTINEL" if val is None else val
            if marker in seen:
                duplicated[i] = True
            else:
                seen.add(marker)
    else:
        for i in range(n - 1, -1, -1):
            val = processed[i]
            marker = "STR_NA_SENTINEL" if val is None else val
            if marker in seen:
                duplicated[i] = True
            else:
                seen.add(marker)
                
    return np.array(duplicated)

# r2py:entity:stri_duplicated_any
def stri_duplicated_any(str_vec):
    # Returns True if any element is duplicated
    return any(stri_duplicated(str_vec))

# r2py:entity:duplicated
def duplicated(x):
    # Standard R duplicated: NA is NOT considered duplicated (returns FALSE for NAs)
    n = len(x)
    res = [False] * n
    seen = set()
    for i in range(n):
        val = x[i]
        if val is None or (isinstance(val, float) and np.isnan(val)):
            continue
        if val in seen:
            res[i] = True
        else:
            seen.add(val)
    return np.array(res)

# Examples
vec1 = ['a', 'b', 'a', np.nan, 'a', np.nan]
# r2py:entity:stri_duplicated
print(stri_duplicated(vec1))
# r2py:entity:stri_duplicated_1
print(stri_duplicated(vec1, from_last=True))
# r2py:entity:stri_duplicated_any
print(stri_duplicated_any(vec1))

# compare the results:
vec2 = ['\u0105', stri_trans_nfkd('\u0105')]
# r2py:entity:stri_duplicated_2
print(stri_duplicated(vec2))
# r2py:entity:duplicated
print(duplicated(vec2))

vec3 = ['gro\u00df', 'GROSS', 'Gro\u00df', 'Gross']
# r2py:entity:stri_duplicated_3
print(stri_duplicated(vec3, strength=1))
# r2py:entity:duplicated_1
print(duplicated(vec3))