# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 2

import pandas as pd

# Load iris dataset
from sklearn.datasets import load_iris
iris_data = load_iris()
df = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
df['Species'] = iris_data.target

# Equivalent to nest(data = !Species)
# r2py:entity:nest
nested_df = df.groupby('Species').apply(lambda x: x.drop('Species', axis=1)).reset_index(name='data')