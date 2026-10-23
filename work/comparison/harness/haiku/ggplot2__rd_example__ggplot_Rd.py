# Translated from <R script> by r2py v0.3.0
# Model: claude-haiku-4-5  ScriptMap entities: 14

import numpy as np
import pandas as pd
from plotnine import *

# r2py:entity:set.seed
np.random.seed(1)

# r2py:entity:sample_df
sample_df = pd.DataFrame({
    'group': pd.Categorical(np.repeat(['a', 'b', 'c'], 10)),
    'value': np.random.normal(size=30)
})

# r2py:entity:group_means_df
group_means_df = sample_df.groupby('group')['value'].mean().reset_index()
group_means_df.columns = ['group', 'group_mean']

# First plot
# r2py:entity:ggplot
(ggplot(data=sample_df, mapping=aes(x='group', y='value')) +
# r2py:entity:geom_point
 geom_point() +
# r2py:entity:geom_point_1
 geom_point(
     mapping=aes(y='group_mean'), data=group_means_df,
     colour='red', size=3
 ))

# Second plot
# r2py:entity:ggplot_1
(ggplot(data=sample_df) +
# r2py:entity:geom_point_2
 geom_point(mapping=aes(x='group', y='value')) +
# r2py:entity:geom_point_3
 geom_point(
     mapping=aes(x='group', y='group_mean'), data=group_means_df,
     colour='red', size=3
 ))

# Third plot
# r2py:entity:ggplot_2
(ggplot() +
# r2py:entity:geom_point_4
 geom_point(mapping=aes(x='group', y='value'), data=sample_df) +
# r2py:entity:geom_point_5
 geom_point(
     mapping=aes(x='group', y='group_mean'), data=group_means_df,
     colour='red', size=3
 ))