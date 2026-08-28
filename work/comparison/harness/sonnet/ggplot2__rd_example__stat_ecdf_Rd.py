# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 15

import numpy as np
import pandas as pd
from plotnine import *

# r2py:entity:set.seed
np.random.seed(1)

# r2py:entity:df
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 3, 100), np.random.normal(0, 10, 100)]),
    'g': ['1'] * 100 + ['2'] * 100
})

# r2py:entity:ggplot
p1 = (ggplot(df, aes('x')) +
# r2py:entity:stat_ecdf
      stat_ecdf(geom='step'))
print(p1)

# r2py:entity:ggplot_1
p2 = (ggplot(df, aes('x')) +
# r2py:entity:stat_ecdf_1
      stat_ecdf(geom='step', pad=False))
print(p2)

# r2py:entity:ggplot_2
p3 = (ggplot(df, aes('x', colour='g')) +
# r2py:entity:stat_ecdf_2
      stat_ecdf())
print(p3)

# r2py:entity:weighted
weighted = pd.DataFrame({
    'x': list(range(1, 11)),
    'weights': [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
})

# r2py:entity:plain
plain = pd.DataFrame({
    'x': np.repeat(weighted['x'].values, weighted['weights'].values)
})

# r2py:entity:ggplot_3
p4 = (ggplot(plain, aes('x')) +
# r2py:entity:stat_ecdf_3
      stat_ecdf(size=1) +
# r2py:entity:stat_ecdf_4
      stat_ecdf(aes(weight='weights'), data=weighted, colour='green'))
print(p4)