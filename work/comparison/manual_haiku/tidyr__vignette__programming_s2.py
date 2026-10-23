# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: programming_s2
# Translated from R to Python

import pandas as pd

# Create iris dataset
iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

# Nest data by species (group all columns except Species into a 'data' column)
nested_iris = iris.groupby('Species').apply(lambda x: x.reset_index(drop=True)).reset_index(level=0)
nested_iris.columns = ['Species', 'data']

# Alternative: create nested structure
nested_iris = pd.DataFrame({
    'Species': iris['Species'].unique()
})
nested_iris['data'] = nested_iris['Species'].apply(
    lambda sp: iris[iris['Species'] == sp].drop('Species', axis=1).reset_index(drop=True)
)

print(nested_iris)
