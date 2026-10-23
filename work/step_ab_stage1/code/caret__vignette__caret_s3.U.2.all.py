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

# r2py:entity:str
def str_obj(obj):
    """Equivalent to R's str() for dataframes/matrices."""
    if isinstance(obj, (pd.DataFrame, np.ndarray)):
        # R's str(matrix) output for createDataPartition:
        # int [1:157, 1] 1 2 3 4 5 7 10 11 12 13 ...
        # - attr(*, "dimnames")=List of 2
        # ..$ : NULL
        # ..$ : chr "Resample1"
        if isinstance(obj, pd.DataFrame):
            rows, cols = obj.shape
            vals = obj.iloc[:, 0].values
            col_name = obj.columns[0]
        else:
            rows, cols = obj.shape
            vals = obj[:, 0]
            col_name = "Resample1"
        
        val_str = " ".join(map(str, vals[:10]))
        print(f"  int [1:{rows}, {cols}] {val_str} ...")
        print(' - attr(*, "dimnames")=List of 2')
        print('  ..$ : NULL')
        print(f'  ..$ : chr "{col_name}"')
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, p=0.75, times=1, list_val=True, groups=None):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # Stratified sampling
    unique_classes = y.unique()
    resamples = []
    
    for _ in range(times):
        indices = []
        for cls in unique_classes:
            cls_indices = y[y == cls].index + 1 # R uses 1-based indexing
            # Calculate sample size for this class
            n_cls = len(cls_indices)
            sample_size = int(np.ceil(n_cls * p))
            # Sample indices
            sampled = np.random.choice(cls_indices, size=sample_size, replace=False)
            indices.extend(sampled)
        
        # Sort indices as caret does
        resamples.append(np.sort(indices))

    if not list_val:
        # Return a matrix-like structure (DataFrame)
        res_mat = np.array(resamples).T
        df_out = pd.DataFrame(res_mat)
        df_out.columns = [f"Resample{i+1}" for i in range(times)]
        return df_out
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# Sonar is already loaded by shim as a DataFrame
# r2py:entity:set.seed
np.random.seed(107)

# inTrain <- createDataPartition(y = Sonar$Class, p = .75, list = FALSE)
inTrain = create_data_partition(
    y=Sonar['Class'],
    p=0.75,
    list_val=False
)

# str(inTrain)
# r2py:entity:str
str_obj(inTrain)