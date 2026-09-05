# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from shiny import App, ui, render

# Python equivalent of stri_trans_char is str.maketrans and translate
# r2py:entity:stri_trans_char
def stri_trans_char(text, old, new):
    table = str.maketrans(old, new)
    return text.translate(table)

# r2py:entity:stri_trans_char
print(stri_trans_char('id.123', '.', '_'))
# r2py:entity:stri_trans_char_1
print(stri_trans_char('babaab', 'ab', '01'))
# r2py:entity:stri_trans_char_2
print(stri_trans_char('GCUACGGAGCUUCGGAGCUAG', 'ACGT', 'TGCA'))