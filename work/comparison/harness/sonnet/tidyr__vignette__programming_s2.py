# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 2

import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame
df['Species'] = df['target'].map(dict(enumerate(iris.target_names)))
df = df.drop(columns='target')

# r2py:entity:nest
nested = df.groupby('Species').apply(lambda x: x.drop(columns='Species').reset_index(drop=True)).groupby(level=0).apply(lambda x: x.reset_index(level=0, drop=True))

# r2py:entity:nest
result = df.groupby('Species').apply(lambda x: x.drop(columns='Species').reset_index(drop=True))
result = result.groupby(level=0).apply(lambda grp: grp.reset_index(level=0, drop=True))

# r2py:entity:nest
nested = (
    df.groupby('Species')
    .apply(lambda x: x.drop(columns='Species').reset_index(drop=True))
    .reset_index(level=1, drop=True)
)

# r2py:entity:nest
result = pd.DataFrame({
    'Species': df['Species'].unique()
})
result['data'] = result['Species'].apply(
    lambda s: df[df['Species'] == s].drop(columns='Species').reset_index(drop=True)
)

print(result)