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

def get_terminal_nodes(model, X):
    """
    Approximate ranger's type="terminalNodes" using sklearn's apply method.
    """
    return model.apply(X)

def csrf(formula, training_data, test_data, params1=None, params2=None, verbose=False):
    if params1 is None: params1 = {}
    if params2 is None: params2 = {}
    
    target_col = formula.split('~')[0].strip()
    
    X_train = training_data.drop(columns=[target_col])
    y_train = training_data[target_col]
    X_test = test_data.drop(columns=[target_col])
    y_test = test_data[target_col]
    
    model1_params = {
        'n_estimators': params1.get('num.trees', 500),
        'max_features': params1.get('mtry', 'sqrt'),
        'random_state': 42 
    }
    rf_proximity = RandomForestClassifier(**model1_params)
    rf_proximity.fit(X_train, y_train)
    
    terminal_nodes_train = get_terminal_nodes(rf_proximity, X_train) 
    terminal_nodes_test = get_terminal_nodes(rf_proximity, X_test)    
    
    predictions = []
    n_test = X_test.shape[0]
    
    for i in range(n_test):
        if verbose:
            print(f"Computing case-specific prediction for test observation {i+1} of {n_test}. ({round((i+1)/n_test * 100, 2)}% complete.)")
        
        test_node_row = terminal_nodes_test[i] 
        matches = (terminal_nodes_train == test_node_row).sum(axis=1) 
        
        sum_matches = matches.sum()
        if sum_matches == 0:
            weights = np.ones(len(matches)) / len(matches)
        else:
            weights = matches / sum_matches
            
        model2_params = {
            'n_estimators': params2.get('num.trees', 500),
            'max_features': params2.get('mtry', 'sqrt'),
            'random_state': 42
        }
        rf_case = RandomForestClassifier(**model2_params)
        rf_case.fit(X_train, y_train, sample_weight=weights)
        
        pred = rf_case.predict(X_test.iloc[[i]])[0]
        predictions.append(pred)
        
    return np.array(predictions)

# Handle indices from shim
iris_df = globals().get('iris')
train_idx_raw = globals().get('train.idx')

# r2py:entity:train.idx
# (Already exists in globals from shim)

# r2py:entity:iris.train
train_idx_0based = [int(i) - 1 for i in train_idx_raw]
iris_train = iris_df.iloc[train_idx_0based].copy()
globals()['iris.train'] = iris_train

# r2py:entity:iris.test
iris_test = iris_df.drop(index=train_idx_0based).copy()
globals()['iris.test'] = iris_test

# r2py:entity:csrf
csrf_results = csrf(
    formula="Species ~ .", 
    training_data=iris_train, 
    test_data=iris_test, 
    params1={'num.trees': 50, 'mtry': 4}, 
    params2={'num.trees': 5}
)
print(csrf_results)