# Translated from <R script> by r2py v0.3.0
# Model: claude-opus-4-6  ScriptMap entities: 15

import numpy as np
import pandas as pd
from plotnine import ggplot, aes, stat_ecdf

# r2py:entity:set.seed
np.random.seed(1)
# r2py:entity:df
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 3, 100), np.random.normal(0, 10, 100)]),
    'g': pd.Categorical(np.repeat([1, 2], 100))
})

# r2py:entity:ggplot
plot1 = (
    ggplot(df, aes(x='x'))
# r2py:entity:stat_ecdf
    + stat_ecdf(geom="step")
)
print(plot1)

# Don't go to positive/negative infinity
# r2py:entity:ggplot_1
plot2 = (
    ggplot(df, aes(x='x'))
# r2py:entity:stat_ecdf_1
    + stat_ecdf(geom="step", pad=False)
)
print(plot2)

# Multiple ECDFs
# r2py:entity:ggplot_2
plot3 = (
    ggplot(df, aes(x='x', colour='g'))
# r2py:entity:stat_ecdf_2
    + stat_ecdf()
)
print(plot3)

# Using weighted eCDF
# r2py:entity:weighted
weighted = pd.DataFrame({
    'x': list(range(1, 11)),
    'weights': list(range(1, 6)) + list(range(5, 0, -1))
})
# r2py:entity:plain
plain = pd.DataFrame({
    'x': np.repeat(weighted['x'].values, weighted['weights'].values)
})

# r2py:entity:ggplot_3
plot4 = (
    ggplot(plain, aes(x='x'))
# r2py:entity:stat_ecdf_3
    + stat_ecdf(size=1)
# r2py:entity:stat_ecdf_4
    + stat_ecdf(
        aes(weight='weights'),
        data=weighted, colour="green"
    )
)
print(plot4)