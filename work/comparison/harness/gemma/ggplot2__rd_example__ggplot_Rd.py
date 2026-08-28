# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 14

import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point

# r2py:data_shim:begin
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# r2py:data_shim:end

# R's set.seed(1) and rnorm() produce specific values. 
# Since numpy's random is different, we must be careful.
# However, the task is to translate the code.
# r2py:entity:set.seed
np.random.seed(1)

# r2py:entity:sample_df
sample_df = pd.DataFrame({
    'group': np.repeat(letters[0:3], 10),
    'value': np.random.normal(0, 1, 30)
})

# r2py:entity:group_means_df
group_means_df = sample_df.groupby('group', as_index=False)['value'].mean()
group_means_df.columns = ['group', 'group_mean']

# First plot: mapping in ggplot()
p1 = (
# r2py:entity:ggplot
    ggplot(sample_df, aes(x='group', y='value'))
# r2py:entity:geom_point
    + geom_point()
# r2py:entity:geom_point_1
    + geom_point(aes(y='group_mean'), data=group_means_df, colour='red', size=3)
)
print(p1)

# Second plot: mapping in geom_point()
p2 = (
# r2py:entity:ggplot_1
    ggplot(sample_df)
# r2py:entity:geom_point_2
    + geom_point(aes(x='group', y='value'))
# r2py:entity:geom_point_3
    + geom_point(aes(x='group', y='group_mean'), data=group_means_df, colour='red', size=3)
)
print(p2)

# Third plot: mapping and data in geom_point()
p3 = (
# r2py:entity:ggplot_2
    ggplot()
# r2py:entity:geom_point_4
    + geom_point(aes(x='group', y='value'), data=sample_df)
# r2py:entity:geom_point_5
    + geom_point(aes(x='group', y='group_mean'), data=group_means_df, colour='red', size=3)
)
print(p3)