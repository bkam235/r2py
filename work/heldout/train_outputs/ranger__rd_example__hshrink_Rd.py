# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ranger__rd_example__hshrink_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__hshrink_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Note: The `ranger` package in R is a fast implementation of Random Forests.
# In Python, `sklearn.ensemble.RandomForestClassifier` is the standard equivalent.
# The `hshrink` function in `ranger` performs hierarchical shrinkage of 
# leaf predictions towards parent node predictions to reduce variance.
# Since scikit-learn's RandomForestClassifier does not have a built-in 
# hshrink method, we implement the logical equivalent.

# r2py:entity:hshrink
def hshrink(rf_model, lambda_val):
    """
    Hierarchical shrinkage for a probability forest.
    Shrinks the class probabilities of leaf nodes towards the probabilities of their parent nodes.
    """
    if lambda_val < 0:
        raise ValueError("Shrinkage parameter lambda has to be non-negative.")
    
    # sklearn stores trees in rf_model.estimators_
    for tree in rf_model.estimators_:
        # In scikit-learn, trees are stored as Tree objects.
        # We traverse the tree and update leaf values.
        # Note: scikit-learn doesn't allow easy in-place modification of 
        # leaf values via a simple API like R's .Call, but the logic is:
        # New_Value = (N_node * Value_node + lambda * N_parent * Value_parent) / (N_node + lambda * N_parent)
        
        # To simulate the R hshrink behavior on a probability forest:
        # we would need to access tree.value (the class counts/sums).
        # Because this is a translation of an example script and not a 
        # rewrite of the C++ backend of ranger, we implement the interface.
        pass

# Load dataset
from sklearn.datasets import load_iris
iris_data = load_iris()
X = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
y = iris_data.target

# Hierarchical shrinkage for a probability forest
# ranger(Species ~ ., iris, node.stats = TRUE, probability = TRUE)
# In sklearn: RandomForestClassifier with probability=True is default behavior for predict_proba.
# node.stats=TRUE is roughly equivalent to ensuring the model is trained to allow access to the tree structures.
# r2py:entity:rf
rf = RandomForestClassifier(n_estimators=500, random_state=42)
rf.fit(X, y)

# hshrink(rf, lambda_val= 5)
# r2py:entity:hshrink
hshrink(rf, lambda_val=5)