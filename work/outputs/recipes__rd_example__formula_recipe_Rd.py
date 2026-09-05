# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__rd_example__formula_recipe_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__formula_recipe_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load iris dataset
from sklearn.datasets import load_iris
iris_data = load_iris()
df = pd.DataFrame(data=iris_data.data, columns=iris_data.feature_names)
df['Species'] = iris_data.target

# r2py:entity:formula
# Equivalent to: recipe(Species + Sepal.Length ~ ., data = iris) |> prep()
# In Python, we define the target and features explicitly
X = df.drop(columns=['Species'])
y = df['Species']

# r2py:entity:recipe
# Equivalent to: recipe(Species ~ ., data = iris) |> step_center(all_numeric()) |> prep()
# step_center in recipes centers the data (subtracts the mean)
# r2py:entity:step_center
scaler = StandardScaler(with_std=False) 
numeric_cols = X.select_dtypes(include=[np.number]).columns
X_centered = X.copy()
# r2py:entity:prep
X_centered[numeric_cols] = scaler.fit_transform(X[numeric_cols])

# r2py:entity:formula_1
# Printing the 'formula' equivalent (the feature names and target)
print(f"Target: Species")
print(f"Features: {list(X.columns)}")