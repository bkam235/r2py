import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ranger__rd_example__csrf_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__csrf_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'train.idx']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(expr):
    return expr

# r2py:entity:import_ranger
def import_ranger():
    pass

suppressPackageStartupMessages(import_ranger())

# r2py:entity:train.idx
train_idx = globals().get('train.idx')

# r2py:entity:iris.train
# Assign directly to the global namespace to match R's variable names
iris_train = iris.iloc[np.array(train_idx) - 1].copy()
globals()['iris.train'] = iris_train

# r2py:entity:iris.test
all_indices = np.arange(1, len(iris) + 1)
test_indices = np.setdiff1d(all_indices, np.array(train_idx))
iris_test = iris.iloc[test_indices - 1].copy()
globals()['iris.test'] = iris_test

def csrf(formula, training_data, test_data, params1=None, params2=None, verbose=False):
    if params1 is None: params1 = {}
    if params2 is None: params2 = {}
    
    target_col = formula.split(' ~ ')[0]
    X_train = training_data.drop(columns=[target_col])
    y_train = training_data[target_col]
    X_test = test_data.drop(columns=[target_col])
    
    rf_proximity = RandomForestClassifier(
        n_estimators=params1.get('num.trees', 500),
        max_features=params1.get('mtry', 'sqrt'),
        random_state=42
    )
    rf_proximity.fit(X_train, y_train)
    
    terminal_node_ids_train = rf_proximity.apply(X_train)
    terminal_node_ids_test = rf_proximity.apply(X_test)
    
    predictions = []
    n_test = len(test_data)
    
    for i in range(n_test):
        if verbose:
            print(f"Computing case-specific prediction for test observation {i+1} of {n_test}. ({round((i+1)/n_test * 100, 2)}% complete.)")
        
        num_same_node = np.sum(terminal_node_ids_train == terminal_node_ids_test[i, :], axis=1)
        total_same = np.sum(num_same_node)
        
        if total_same == 0:
            weights = np.ones(len(y_train)) / len(y_train)
        else:
            weights = num_same_node / total_same
            
        rf_case = RandomForestClassifier(
            n_estimators=params2.get('num.trees', 500),
            max_features=params2.get('mtry', 'sqrt'),
            random_state=42
        )
        rf_case.fit(X_train, y_train, sample_weight=weights)
        
        pred = rf_case.predict(X_test.iloc[[i]])[0]
        predictions.append(pred)
        
    return np.array(predictions)

# r2py:entity:csrf
csrf_results = csrf(
    formula="Species ~ .", 
    training_data=iris_train, 
    test_data=iris_test, 
    params1={'num.trees': 50, 'mtry': 4}, 
    params2={'num.trees': 5}
)

# Match R's output format for character vectors: 
# [1] setosa setosa ...
# [7] setosa setosa ...
res_list = list(csrf_results)
for i in range(0, len(res_list), 6):
    chunk = res_list[i:i+6]
    idx = i + 1
    print(f"[{idx}] {'  '.join(chunk)}")