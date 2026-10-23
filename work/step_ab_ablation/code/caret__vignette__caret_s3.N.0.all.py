# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__vignette__caret_s3.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sonar']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

def createDataPartition(y, p=0.75, list_val=False, times=1):
    """
    Python equivalent to caret::createDataPartition.
    Stratified sampling of indices.
    """
    y = pd.Series(y)
    # R indices are 1-based
    indices = np.arange(1, len(y) + 1)
    
    # Handle stratification
    unique_classes = y.unique()
    resamples = []
    
    for t in range(times):
        selected_indices = []
        for cls in unique_classes:
            cls_indices = indices[y == cls]
            # R's createDataPartition uses ceiling(nrow * p)
            n_sample = int(np.ceil(len(cls_indices) * p))
            # Sample without replacement
            sampled = np.random.choice(cls_indices, size=n_sample, replace=False)
            selected_indices.extend(sampled)
        
        # The result for each resample is sorted
        resamples.append(np.sort(selected_indices))
    
    if not list_val:
        # Return as a matrix (numpy array or DataFrame)
        # In R, list=FALSE returns a matrix where each column is a resample
        return np.array(resamples).T
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

def str_r(obj):
    """Approximation of R's str() for the resulting matrix."""
    if isinstance(obj, np.ndarray):
        rows, cols = obj.shape
        # The output of str() for a matrix of integers typically looks like:
        # num [1:157, 1] 1 2 5 ...
        # Note: createDataPartition indices are integers, but R's str() often labels them 'int' or 'num'
        prefix = "int" if np.issubdtype(obj.dtype, np.integer) else "num"
        # Format the dimensions [1:rows, 1:cols]
        dim_str = f"[{1}:{rows}, {1}:{cols}]"
        # Get a few values from the first column
        vals = obj[:6, 0]
        val_str = " ".join(map(str, vals))
        print(f"{prefix} {dim_str} {val_str} ...")
    else:
        print(repr(obj))

# set.seed(107)
np.random.seed(107)

# inTrain <- createDataPartition(y = Sonar$Class, p = .75, list = FALSE)
inTrain = createDataPartition(
    y=Sonar['Class'],
    p=0.75,
    list_val=False
)

# str(inTrain)
str_r(inTrain)