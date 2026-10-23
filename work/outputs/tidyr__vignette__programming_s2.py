# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 2

import pandas as pd
from sklearn.datasets import load_iris

# Load the iris dataset as a pandas DataFrame
iris_data = load_iris()
iris = pd.DataFrame(data=iris_data.data, columns=iris_data.feature_names)
iris['Species'] = iris_data.target

# In R's tidyr, nest(data = !Species) nests all columns except 'Species'.
# In pandas, this is achieved by grouping by the desired key and 
# applying a function that converts the remaining group into a DataFrame.
# r2py:entity:nest
iris_nested = iris.groupby('Species').apply(lambda x: x.drop(columns=['Species'])).unstack()

# However, to strictly replicate the 'nested' structure where a column 
# contains dataframes (similar to tidyr::nest), we do:
# r2py:entity:nest
iris_nested = (
    iris.groupby('Species')
    .apply(lambda x: x.drop(columns=['Species']))
    .reset_index(level=0)
    .rename(columns={0: 'data'})
)

# Since the R code specified `nest(data = !Species)`, 
# the result is a dataframe with 'Species' and a 'data' column containing the other values.
# A more direct idiomatic pandas approach for this specific logic:
# r2py:entity:nest
iris_nested = iris.groupby('Species').apply(lambda x: x.drop(columns=['Species'])).reset_index(level=0).rename(columns={0: 'data'})

# To match the tidyr output precisely (where 'data' is a list of dataframes):
# r2py:entity:nest
iris_nested = (
    iris.groupby('Species')
    .apply(lambda x: x.drop(columns=['Species']))
    .reset_index()
    .rename(columns={'level_1': 'data'}) # This depends on pandas version
)

# Correct Pythonic way to mimic tidyr::nest for the provided R snippet:
# r2py:entity:nest
iris_nested = iris.groupby('Species').apply(lambda x: x.drop(columns=['Species'])).reset_index(level=0).rename(columns={0: 'data'})
# In newer pandas versions, the apply result can be tricky. The most robust way to get "nested" dataframes:
# r2py:entity:nest
iris_nested = pd.DataFrame({
    'Species': iris['Species'].unique(),
    'data': [iris[iris['Species'] == s].drop(columns=['Species']) for s in iris['Species'].unique()]
})

print(iris_nested)