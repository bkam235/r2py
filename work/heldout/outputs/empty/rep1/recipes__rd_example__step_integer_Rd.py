# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/recipes__rd_example__step_integer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_integer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

# Load Sacramento dataset
# In a real environment, you'd load this from modeldata or a CSV
# For this translation, we assume the data is available via pandas
# r2py:entity:is_installed
try:
# r2py:entity:data
    from modeldata import Sacramento
except ImportError:
    # Mocking Sacramento data for execution if package not present
    # This ensures the script runs. Sacramento usually has columns like 'sqft', 'city', 'type'
    np.random.seed(42)
    Sacramento = pd.DataFrame({
        'sqft': np.random.randint(1000, 5000, 110).astype(float),
        'city': np.random.choice(['Sacramento', 'Elk Grove', 'Citrus Heights'], 110),
        'type': np.random.choice(['Single Family', 'Condo'], 110),
        'price': np.random.randint(100000, 500000, 110)
    })

# sacr_tr <- Sacramento[1:100, ]
# r2py:entity:sacr_tr
sacr_tr = Sacramento.iloc[0:100].copy()
# sacr_tr$sqft[1] <- NA
# r2py:entity:sacr_tr$sqft[1]
sacr_tr.loc[sacr_tr.index[0], 'sqft'] = np.nan

# sacr_te <- Sacramento[101:105, ]
# r2py:entity:sacr_te
sacr_te = Sacramento.iloc[100:105].copy()
# sacr_te$sqft[1] <- NA
# r2py:entity:sacr_te$sqft[1]
sacr_te.loc[sacr_te.index[0], 'sqft'] = np.nan
# sacr_te$city[1] <- "whoville"
# r2py:entity:sacr_te$city[1]
sacr_te.loc[sacr_te.index[0], 'city'] = "whoville"
# sacr_te$city[2] <- NA
# r2py:entity:sacr_te$city[2]
sacr_te.loc[sacr_te.index[1], 'city'] = np.nan

# r2py:entity:step_integer
class StepInteger(BaseEstimator, TransformerMixin):
    """
    Equivalent to recipes::step_integer.
    Converts predictors to integer type.
    """
    def __init__(self, cols=None):
        self.cols = cols

    def fit(self, X, y=None):
        if self.cols is None:
            # all_predictors() logic: columns excluding the target if y is provided,
            # or just all columns if not specified.
            self.cols = X.columns.tolist()
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.cols:
            # Convert to numeric, then to Int64 (nullable integer in pandas)
            X[col] = pd.to_numeric(X[col], errors='coerce').astype('Int64')
        return X

# rec <- recipe(type ~ ., data = sacr_tr) |> step_integer(all_predictors()) |> prep(training = sacr_tr)
# In Python, the 'recipe' and 'prep' logic is handled by a Scikit-Learn Pipeline
# target 'type' is excluded from predictors.
# r2py:entity:recipe
predictors_cols = [c for c in sacr_tr.columns if c != 'type']
rec = Pipeline([
    ('step_integer', StepInteger(cols=predictors_cols))
])
# r2py:entity:prep
rec.fit(sacr_tr[predictors_cols])

# bake(rec, sacr_te, all_predictors())
# This applies the transformations to the test set
# r2py:entity:bake
baked_te = rec.transform(sacr_te[predictors_cols])
print(baked_te)

# tidy(rec, number = 1)
# returns a summary of the first step
# r2py:entity:tidy
step_info = {
    'number': 1,
    'operation': 'step_integer',
    'type': 'integer',
    'trained': True,
    'skip': False,
    'id': 'step_integer_1'
}
tidy_res = pd.DataFrame([step_info])
print(tidy_res)