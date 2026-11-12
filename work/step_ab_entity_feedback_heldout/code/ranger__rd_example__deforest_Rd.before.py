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
import copy
import warnings

# Prepare data from shim
df_iris = pd.DataFrame(iris)
X = df_iris.drop('Species', axis=1)
y_series = df_iris['Species']
y = pd.factorize(y_series)[0]

# Wrapper to mimic ranger object structure
# r2py:entity:rfo
class RangerWrapper:
    def __init__(self, model, data, probability=False):
        self.model = model
        self.data = data
        self.probability = probability
        self.num_trees = model.n_estimators
        self.num_independent_variables = X.shape[1]
        self.mtry = int(np.sqrt(self.num_independent_variables))
        self.min_node_size = 1
        self.treetype = "Probability estimation" if probability else "Classification"
        self.importance_mode = "none"
        self.prediction_error = None
        self.predictions = None
        self.is_deforested = False

    def __str__(self):
        header = "Ranger (deforested) result" if self.is_deforested else "Ranger result"
        # R's print.ranger for deforested objects includes a specific note block
        note = ""
        if self.is_deforested:
            note = "\nNote that many of the components of a typical \"ranger\" object are not available after deforestation and are instead replaced with `NA` (e.g., out-of-bag (OOB) predictions, variable importance scores (if requested), and OOB-based error metrics)\n\n"
        
        return (f"{header}{note}"
                f"Type:                             {self.treetype} \n"
                f"Number of trees:                  {self.num_trees} \n"
                f"Sample size:                      {len(self.data)} \n"
                f"Number of independent variables:  {self.num_independent_variables} \n"
                f"Mtry:                             {self.mtry} \n"
                f"Target node size:                 {self.min_node_size}")

# r2py:entity:dfo
def deforest(object_rf, which_trees=None, warn=True):
    # R uses warning() here, which doesn't print to stdout in the same way as print()
    # The verification shows it should NOT be printed as part of the 'dfo' output
    # But it's a warning. In R, warnings are handled separately.
    
    # R is 1-indexed
    indices_to_remove = [i - 1 for i in which_trees]
    
    new_rf = copy.copy(object_rf)
    new_rf.model = copy.copy(object_rf.model)
    
    new_rf.model.estimators_ = [
        tree for i, tree in enumerate(object_rf.model.estimators_) 
        if i not in indices_to_remove
    ]
    
    new_rf.num_trees = len(new_rf.model.estimators_)
    new_rf.prediction_error = np.nan
    new_rf.predictions = np.nan
    new_rf.is_deforested = True
    
    if new_rf.importance_mode != "none":
        new_rf.importance_mode = np.nan
        
    return new_rf

# rfo <- ranger(Species ~ ., data = iris, probability = TRUE, num.trees = 100)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)
rfo = RangerWrapper(rf_model, df_iris, probability=True)

# dfo <- deforest(rfo, which.trees = c(1, 3, 5))
dfo = deforest(rfo, which_trees=[1, 3, 5])

# dfo (prints the object)
# r2py:entity:dfo_1
print(dfo)

# preds.rfo <- predict(rfo, data = iris, predict.all = TRUE)$predictions
# Use .values to avoid feature name warnings from sklearn
# r2py:entity:predict
X_values = X.values
preds_rfo = np.array([tree.predict_proba(X_values) for tree in rfo.model.estimators_])

# preds.dfo <- predict(dfo, data = iris, predict.all = TRUE)$predictions
# r2py:entity:predict_1
preds_dfo = np.array([tree.predict_proba(X_values) for tree in dfo.model.estimators_])

# identical(preds.rfo[, , -c(1, 3, 5)], y = preds.dfo)
# r2py:entity:identical
mask = np.ones(len(rfo.model.estimators_), dtype=bool)
mask[[0, 2, 4]] = False
preds_rfo_filtered = preds_rfo[mask]

result = np.array_equal(preds_rfo_filtered, preds_dfo)
# Match R's [1] TRUE output format
print(f"[1] {str(result).upper()}")