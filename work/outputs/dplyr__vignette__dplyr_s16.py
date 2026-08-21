# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *

# Load dataset (assuming starwars is provided as a pandas DataFrame)
# In a real scenario, you would load it via a library or CSV
# For this translation, we assume 'starwars' is already defined as a DataFrame
starwars = pd.DataFrame({
    'height': [170, 180, 160],
    'mass': [70, 80, 60],
    'name': ['Luke', 'Han', 'Leia']
})

# Transformation logic
result = (
    starwars
# r2py:entity:mutate
    .assign(
        height_m = lambda df: df['height'] / 100,
        BMI = lambda df: df['mass'] / (df['height_m']**2)
    )
# r2py:entity:select
    .pipe(lambda df: df[['BMI'] + [col for col in df.columns if col != 'BMI']])
)

print(result)