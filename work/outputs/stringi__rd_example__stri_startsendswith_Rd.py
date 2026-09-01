# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import re
import pandas as pd
import numpy as np

# r2py:entity:stri_startswith_charclass
# stri_startswith_charclass(' trim me! ', '\\p{WSpace}')
# \s matches any whitespace character
print(bool(re.match(r'\s', ' trim me! ')))

# r2py:entity:stri_startswith_fixed
# stri_startswith_fixed(c('a1', 'a2', 'b3', 'a4', 'c5'), 'a')
data = ['a1', 'a2', 'b3', 'a4', 'c5']
print([s.startswith('a') for s in data])

# r2py:entity:stri_detect_regex
# stri_detect_regex(c('a1', 'a2', 'b3', 'a4', 'c5'), '^a')
print([bool(re.search(r'^a', s)) for s in data])

# r2py:entity:stri_startswith_fixed_1
# stri_startswith_fixed('ababa', 'ba')
print('ababa'.startswith('ba'))

# r2py:entity:stri_startswith_fixed_2
# stri_startswith_fixed('ababa', 'ba', from_val=2)
# In R, from_val=2 is 1-indexed (the second character), so we slice from index 1
print('ababa'[1:].startswith('ba'))

# r2py:entity:stri_startswith_coll
# stri_startswith_coll(c('a1', 'A2', 'b3', 'A4', 'C5'), 'a', strength=1)
# strength=1 usually means case-insensitive
data_coll = ['a1', 'A2', 'b3', 'A4', 'C5']
print([s.lower().startswith('a') for s in data_coll])

# r2py:entity:pat
# pat <- stri_paste(...)
pat = '\u0635\u0644\u0649 \u0627\u0644\u0644\u0647 ' + '\u0639\u0644\u064a\u0647 \u0648\u0633\u0644\u0645XYZ'

# r2py:entity:stri_endswith_coll
# stri_endswith_coll('\ufdfa\ufdfa\ufdfaXYZ', pat, strength=1)
print('\ufdfa\ufdfa\ufdfaXYZ'.lower().endswith(pat.lower()))