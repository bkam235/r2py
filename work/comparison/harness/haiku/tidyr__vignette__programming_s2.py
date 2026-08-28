# Translated from <R script> by r2py v0.3.0
# Model: claude-haiku-4-5  ScriptMap entities: 2

import pandas as pd

iris = pd.read_csv('iris.csv')  # Assuming iris data is available as CSV

# r2py:entity:nest
nested_iris = iris.groupby('Species').apply(
    lambda x: x.drop('Species', axis=1)
).reset_index().rename(columns={0: 'data'})

# Alternative approach using a dictionary structure:
nested_iris = pd.DataFrame({
    'Species': iris['Species'].unique(),
    'data': [iris[iris['Species'] == species].drop('Species', axis=1).reset_index(drop=True) 
             for species in iris['Species'].unique()]
})

print(nested_iris)