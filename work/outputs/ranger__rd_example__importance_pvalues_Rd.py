# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ranger__rd_example__importance_pvalues_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__importance_pvalues_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Simulation part
# r2py:entity:n
n = 50
# r2py:entity:p
p = 400
# r2py:entity:dat
y = np.random.binomial(1, 0.5, n)
X = np.random.uniform(0, 1, (n, p))
dat = pd.DataFrame(X, columns=[f'V{i}' for i in range(p)])
dat['y'] = y

# Fit Random Forest
# r2py:entity:rf.sim
rf_sim = RandomForestClassifier(importance='impurity')
rf_sim.fit(dat.drop('y', axis=1), dat['y'])
# Note: Python sklearn does not have a direct equivalent to ranger's importance_pvalues 
# (Janitza/Altmann methods). We provide the raw importances.
# r2py:entity:importance_pvalues
sim_importance = rf_sim.feature_importances_

# Iris part
# r2py:entity:rf.iris
iris_data = load_iris()
X_iris = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
y_iris = iris_data.target

rf_iris = RandomForestClassifier()
rf_iris.fit(X_iris, y_iris)
# r2py:entity:importance_pvalues_1
iris_importance = rf_iris.feature_importances_