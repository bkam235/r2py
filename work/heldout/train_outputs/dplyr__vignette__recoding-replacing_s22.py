# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np

# Creating the tibble equivalent
# r2py:entity:likert
likert = pd.DataFrame({
    'score': [0, 1, 2, 2, 4, 5, 2, 3, 1, 4]
})

try:
    # Assuming 'lookup' is a predefined mapping (DataFrame/Dictionary)
    # In R, lookup$from and lookup$to implies a mapping table.
    # we create a dictionary from lookup for the .map() function.
# r2py:entity:mutate
    mapping = dict(zip(lookup['from'], lookup['to']))
    
    # mutate + recode_values approximation
    likert['score'] = likert['score'].map(mapping).fillna("error")
    
except NameError:
    # Handle case where 'lookup' is not defined in the environment
    pass