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
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# r2py:entity:hshrink
def hshrink(rf_model, lambda_val):
    """
    Hierarchical shrinkage for a probability forest.
    Shrinks leaf node class probabilities towards parent node probabilities.
    Formula: New_Value = (N_node * Value_node + lambda * N_parent * Value_parent) / (N_node + lambda * N_parent)
    """
    if lambda_val < 0:
        raise ValueError("Shrinkage parameter lambda has to be non-negative.")
    
    for tree in rf_model.estimators_:
        # tree.value: array of shape (n_nodes, n_outputs, n_classes)
        # tree.n_node_samples: array of shape (n_nodes,)
        # tree.children_left, tree.children_right: indices of children
        
        # We need to traverse from root down to update child nodes based on parents.
        # The root is index 0.
        stack = [0]
        while stack:
            parent = stack.pop()
            left = tree.children_left[parent]
            right = tree.children_right[parent]
            
            for child in [left, right]:
                if child != -1: # If it's not a leaf
                    # This is simplified. In R's ranger, hshrink updates the leaf values.
                    # We need to find the leaves and shrink them.
                    stack.append(child)
                    
        # To actually implement hshrink in sklearn, we must identify leaf nodes
        # and update their .value based on their parent's .value.
        # Scikit-learn doesn't store parent pointers, so we traverse.
        
        node_values = tree.value.copy()
        node_samples = tree.n_node_samples
        
        def traverse(node_idx, parent_val, parent_samples):
            nonlocal node_values
            # If leaf
            if tree.children_left[node_idx] == -1:
                # apply shrinkage: (N_node * Val_node + lambda * N_parent * Val_parent) / (N_node + lambda * N_parent)
                # Note: node_values[node_idx] is (1, n_classes)
                current_val = node_values[node_idx]
                current_samples = node_samples[node_idx]
                
                # Weighting
                weight_node = current_samples
                weight_parent = lambda_val * parent_samples
                
                new_val = (weight_node * current_val + weight_parent * parent_val) / (weight_node + weight_parent)
                node_values[node_idx] = new_val
            else:
                # Not a leaf, pass current value as parent for children
                current_val = node_values[node_idx]
                current_samples = node_samples[node_idx]
                traverse(tree.children_left[node_idx], current_val, current_samples)
                traverse(tree.children_right[node_idx], current_val, current_samples)

        # Start traversal from root
        # Root has no parent in the shrink sense, or we treat it as the base.
        # The R hshrink usually applies to leaves.
        root_val = node_values[0]
        root_samples = node_samples[0]
        
        # We need to implement this iteratively to avoid recursion depth issues
        stack = [(0, root_val, root_samples)]
        while stack:
            curr, p_val, p_samp = stack.pop()
            if tree.children_left[curr] == -1: # Leaf
                c_val = node_values[curr]
                c_samp = node_samples[curr]
                w_node = c_samp
                w_parent = lambda_val * p_samp
                node_values[curr] = (w_node * c_val + w_parent * p_val) / (w_node + w_parent)
            else:
                c_val = node_values[curr]
                c_samp = node_samples[curr]
                stack.append((tree.children_left[curr], c_val, c_samp))
                stack.append((tree.children_right[curr], c_val, c_samp))
        
        tree.value = node_values

# Use the iris dataset provided by shim
X = iris.drop(columns=['Species'])
y = iris['Species']

# r2py:entity:rf
# ranger(Species ~ ., iris, node.stats = TRUE, probability = TRUE)
# probability=True in ranger returns class probabilities.
# n_estimators is not specified in R's ranger default for the example, but defaults to 500.
rf = RandomForestClassifier(n_estimators=500, random_state=42)
rf.fit(X, y)

# hshrink(rf, lambda = 5)
hshrink(rf, lambda_val=5)