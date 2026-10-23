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
    if isinstance(obj, pd.DataFrame):
        rows, cols = obj.shape
        # We simulate the output: int [1:157, 1] 1 2 3 4 5 7 10 11 12 13 ...
        # Using the values of the first column
        vals = obj.iloc[:, 0].values
        val_str = " ".join(map(str, vals[:10]))
        print(f"  int [1:{rows}, 1] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print(f"  ..$ : chr \"{obj.columns[0]}\"")
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, p=0.75, list_val=False, times=1):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # Group indices by class
    indices_by_class = y.groupby(y).groups
    
    resamples = []
    for _ in range(times):
        sampled_indices = []
        for group_indices in indices_by_class.values():
            # Calculate number of samples for this class: ceil(len(group) * p)
            num = int(np.ceil(len(group_indices) * p))
            # Sample indices. We use a local random state or consistent seed.
            # To match R's sample() under set.seed, we must be careful.
            # R's sample is not easily replicated by np.random.choice exactly.
            # However, we must implement the logic.
            group_array = np.array(group_indices)
            perm = np.random.permutation(group_array)
            sampled_indices.extend(perm[:num])
        
        # caret sorts the resulting indices
        resamples.append(np.sort(np.array(sampled_indices) + 1)) # +1 for R 1-based indexing

    if not list_val:
        # Return as a DataFrame to mimic the matrix return
        res_mat = np.array(resamples).T
        df_out = pd.DataFrame(res_mat, columns=[f"Resample{i+1}" for i in range(times)])
        return df_out
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# set.seed(107)
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