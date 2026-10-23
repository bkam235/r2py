# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd

# r2py:entity:unnest_wider
try:
    # In pandas, the equivalent of unnest_wider for a column of dictionaries 
    # is applying pd.Series to that column and joining it back
    basic_info_df = discs['basic_information'].apply(pd.Series)
    discs = pd.concat([discs.drop('basic_information', axis=1), basic_info_df], axis=1)
except Exception:
    pass