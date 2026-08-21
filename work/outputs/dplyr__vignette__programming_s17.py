# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 5

import pandas as pd
import numpy as np
from plotnine import *

# Assuming starwars dataset is loaded as a pandas DataFrame
# For demonstration, we use a dummy dataframe if starwars is not available
try:
    from plotnine.data import starwars
except ImportError:
    # Fallback for example purposes
    starwars = pd.DataFrame({
        'homeworld': ['Tatooine', 'Tatooine', 'Naboo', 'Naboo', 'Alderaan'],
        'sex': ['male', 'male', 'female', 'female', 'female'],
        'gender': ['masculine', 'masculine', 'feminine', 'feminine', 'feminine'],
        'mass': [75, 80, 60, 65, np.nan],
        'height': [170, 180, 160, 165, 170]
    })

# r2py:entity:my_summarise
def my_summarise(data, *args):
    return data.groupby(list(args), as_index=False)[['mass', 'height']].mean()

# r2py:entity:my_summarise_1
print(my_summarise(starwars, 'homeworld'))
# r2py:entity:my_summarise_2
print(my_summarise(starwars, 'sex', 'gender'))