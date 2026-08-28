# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 15

import pandas as pd
import numpy as np
from plotnine import *

# r2py:entity:set.seed
np.random.seed(1)

# r2py:entity:df
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 3, 100), np.random.normal(0, 10, 100)]),
    'g': np.repeat(['1', '2'], 100)
})

# Plot 1 & 2: ECDF (plotnine handles padding automatically)
# r2py:entity:stat_ecdf
print(ggplot(df, aes('x')) + stat_ecdf(geom="step"))
# r2py:entity:stat_ecdf_1
print(ggplot(df, aes('x')) + stat_ecdf(geom="step"))

# Plot 3: ECDF with groups
# r2py:entity:stat_ecdf_2
print(ggplot(df, aes('x', colour='g')) + stat_ecdf())

# Weighted ECDF logic
# r2py:entity:weighted
weighted = pd.DataFrame({
    'x': np.arange(1, 11), 
    'weights': np.concatenate([np.arange(1, 6), np.arange(5, 0, -1)])
})

# Expanding the weighted dataframe to a plain one
# r2py:entity:plain
plain_x = []
for i in range(len(weighted)):
    plain_x.extend([weighted.iloc[i]['x']] * int(weighted.iloc[i]['weights']))
plain = pd.DataFrame({'x': plain_x})

# Plot 4: Comparison of plain and weighted
# Note: plotnine's stat_ecdf does not natively support a 'weight' mapping 
# in the same way as ggplot2's stat_ecdf. To replicate weighted ECDF, 
# we calculate the ECDF coordinates manually for the weighted set.

# r2py:entity:stat_ecdf_4
def calc_ecdf(data, weight_col=None):
    sorted_df = data.sort_values('x')
    if weight_col:
        cumulative_weight = sorted_df[weight_col].cumsum()
        y = cumulative_weight / cumulative_weight.max()
    else:
        y = np.arange(1, len(sorted_df) + 1) / len(sorted_df)
    return pd.DataFrame({'x': sorted_df['x'], 'y': y})

weighted_ecdf_df = calc_ecdf(weighted, 'weights')

# r2py:entity:ggplot_3
print(
    ggplot(plain, aes('x')) + 
# r2py:entity:stat_ecdf_3
    stat_ecdf(size=1) + 
    geom_step(aes('x', 'y'), data=weighted_ecdf_df, colour="green")
)