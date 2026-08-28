# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 14

import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_point
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# r2py:data_shim:begin
import os, pickle
_shim = os.environ.get('R2PY_DATA_SHIM', '')
if _shim and os.path.exists(_shim):
    with open(_shim, 'rb') as _f:
        _data = pickle.load(_f)
    letters = _data.get('letters', list('abcdefghijklmnopqrstuvwxyz'))
else:
    letters = list('abcdefghijklmnopqrstuvwxyz')
# r2py:data_shim:end

# r2py:entity:set.seed
np.random.seed(1)

# r2py:entity:sample_df
sample_df = pd.DataFrame({
    'group': pd.Categorical(np.repeat(letters[:3], 10)),
    'value': np.random.normal(size=30)
})

# r2py:entity:group_means_df
group_means_df = sample_df.groupby('group', observed=True)['value'].mean().reset_index()
group_means_df.columns = ['group', 'group_mean']

# Pattern 1
plot1 = (
# r2py:entity:ggplot
    ggplot(sample_df, aes(x='group', y='value'))
# r2py:entity:geom_point
    + geom_point()
# r2py:entity:geom_point_1
    + geom_point(aes(y='group_mean'), data=group_means_df, colour='red', size=3)
)
fig1 = plot1.draw()
plt.close('all')

# Pattern 2
plot2 = (
# r2py:entity:ggplot_1
    ggplot(sample_df)
# r2py:entity:geom_point_2
    + geom_point(aes(x='group', y='value'))
# r2py:entity:geom_point_3
    + geom_point(aes(x='group', y='group_mean'), data=group_means_df, colour='red', size=3)
)
fig2 = plot2.draw()
plt.close('all')

# Pattern 3
plot3 = (
# r2py:entity:ggplot_2
    ggplot()
# r2py:entity:geom_point_4
    + geom_point(aes(x='group', y='value'), data=sample_df)
# r2py:entity:geom_point_5
    + geom_point(aes(x='group', y='group_mean'), data=group_means_df, colour='red', size=3)
)
print(plot3)