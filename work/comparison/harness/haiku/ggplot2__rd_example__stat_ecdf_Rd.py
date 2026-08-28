# Translated from <R script> by r2py v0.3.0
# Model: claude-haiku-4-5  ScriptMap entities: 15

import numpy as np
import pandas as pd
from plotnine import *
import warnings
warnings.filterwarnings('ignore')

# Set seed for reproducibility
# r2py:entity:set.seed
np.random.seed(1)

# Create first dataset
# r2py:entity:df
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 3, 100), np.random.normal(0, 10, 100)]),
    'g': np.repeat([1, 2], 100)
})

# Plot 1: ECDF with step geom
# r2py:entity:stat_ecdf
print(ggplot(df, aes('x')) +
      stat_ecdf(geom='step'))

# Plot 2: ECDF with step geom, pad=False
# r2py:entity:stat_ecdf_1
print(ggplot(df, aes('x')) +
      stat_ecdf(geom='step', pad=False))

# Plot 3: ECDF by group
# r2py:entity:stat_ecdf_2
print(ggplot(df, aes('x', colour='factor(g)')) +
      stat_ecdf())

# Create weighted dataset
# r2py:entity:weighted
weighted = pd.DataFrame({
    'x': range(1, 11),
    'weights': [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
})

# r2py:entity:plain
plain = pd.DataFrame({
    'x': np.repeat(weighted['x'].values, weighted['weights'].values)
})

# Plot 4: Weighted ECDF
# r2py:entity:stat_ecdf_4
print(ggplot(plain, aes('x')) +
      stat_ecdf(size=1) +
      stat_ecdf(
          aes(weight='weights'),
          data=weighted,
          colour='green'
      ))