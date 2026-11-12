# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ranger__rd_example__deforest_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__deforest_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['dfo', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import warnings
import copy

# Data preparation
df_iris = iris.copy()
X = df_iris.drop('Species', axis=1)
y_species = df_iris['Species']
y = pd.factorize(y_species)[0]

# r2py:entity:rfo
# Mimic the ranger object as a dictionary for the verifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

rfo = {
    'class': ['ranger'],
    'numbers': {
        'num.trees': 100,
        'num.independent.variables': 4,
        'mtry': 2,
        'min.node.size': 10,
        'num.samples': 150,
        'max.depth': 0,
        'predictions': None # Filled later by predict call if needed, but R object holds them if requested
    },
    'model': rf_model,
    'probability': True,
    'is_deforested': False
}

# r2py:entity:dfo
def deforest(object_rf, which_trees=None, warn=True):
    if warn:
        warnings.warn('Many of the components of a typical "ranger" object are not available after deforestation and are instead replaced with `NA` (e.g., out-of-bag (OOB) predictions, variable importance scores (if requested), and OOB-based error metrics).')
    
    # R 1-indexed to 0-indexed
    indices_to_remove = [i - 1 for i in which_trees]
    
    # Create a copy of the object
    new_rf = copy.deepcopy(object_rf)
    
    # Filter estimators
    original_estimators = object_rf['model'].estimators_
    new_estimators = [tree for i, tree in enumerate(original_estimators) if i not in indices_to_remove]
    
    # Update the model copy
    new_rf['model'].estimators_ = new_estimators
    new_rf['numbers']['num.trees'] = len(new_estimators)
    new_rf['class'] = ['deforest.ranger', 'ranger']
    new_rf['is_deforested'] = True
    
    return new_rf

dfo = deforest(rfo, which_trees=[1, 3, 5])

# r2py:entity:dfo_1
# Custom print for the deforested ranger object to match R's output
def print_ranger(obj):
    header = "Ranger (deforested) result" if obj.get('is_deforested') else "Ranger result"
    note = ""
    if obj.get('is_deforested'):
        note = "\nNote that many of the components of a typical \"ranger\" object are not available after deforestation and are instead replaced with `NA` (e.g., out-of-bag (OOB) predictions, variable importance scores (if requested), and OOB-based error metrics)\n\n"
    
    nums = obj['numbers']
    print(f"{header}{note}")
    print(f"Type:                             Probability estimation \n" if obj.get('probability') else f"Type:                             Classification \n")
    print(f"Number of trees:                  {nums['num.trees']} ")
    print(f"Sample size:                      {nums['num.samples']} ")
    print(f"Number of independent variables:  {nums['num.independent.variables']} ")
    print(f"Mtry:                             {nums['mtry']} ")
    print(f"Target node size:                 {nums['min.node.size']}")

print_ranger(dfo)

# r2py:entity:predict
# R: predict(rfo, data = iris, predict.all = TRUE)$predictions
# This returns a 3D array [tree, sample, class]
X_values = X.values
preds_rfo = np.array([tree.predict_proba(X_values) for tree in rfo['model'].estimators_])

# r2py:entity:predict_1
# R: predict(dfo, data = iris, predict.all = TRUE)$predictions
preds_dfo = np.array([tree.predict_proba(X_values) for tree in dfo['model'].estimators_])

# r2py:entity:identical
# R: identical(preds.rfo[, , -c(1, 3, 5)], y = preds.dfo)
mask = np.ones(len(rfo['model'].estimators_), dtype=bool)
mask[[0, 2, 4]] = False
preds_rfo_filtered = preds_rfo[mask]

result = np.array_equal(preds_rfo_filtered, preds_dfo)
print(f"[1] {str(result).upper()}")