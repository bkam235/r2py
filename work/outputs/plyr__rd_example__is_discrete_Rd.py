# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# r2py:entity:is.discrete
def is_discrete(x):
    # In Python/Pandas, discrete variables are typically 
    # represented by integer types, categories, or object types.
    if isinstance(x, (list, np.ndarray)):
        x = pd.Series(x)
    
    if pd.api.types.is_integer_dtype(x) or \
       pd.api.types.is_categorical_dtype(x) or \
       pd.api.types.is_object_dtype(x):
        return True
    return False

# r2py:entity:is.discrete
print(is_discrete(np.arange(1, 11)))
# r2py:entity:is.discrete_1
print(is_discrete(["a", "b", "c"]))
# r2py:entity:is.discrete_2
print(is_discrete(pd.Categorical(["a", "b", "c"])))