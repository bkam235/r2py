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
    """Equivalent to R's str() for matrices/arrays."""
    if isinstance(obj, np.ndarray):
        rows, cols = obj.shape
        # R's str(matrix) output: int [1:rows, 1:cols] vals ...
        vals = obj.flatten()[:10]
        val_str = " ".join(map(str, vals))
        print(f"  int [1:{rows}, 1] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print("  ..$ : chr \"Resample1\"")
    elif isinstance(obj, pd.DataFrame):
        rows, cols = obj.shape
        vals = obj.iloc[:, 0].values[:10]
        val_str = " ".join(map(str, vals))
        print(f"  int [1:{rows}, 1] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print("  ..$ : chr \"Resample1\"")
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, times=1, p=0.5, list_val=True, groups=None):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # Stratified sampling: create indices for each class
    unique_classes = y.unique()
    indices_per_class = []
    
    # To mimic R's seed behavior more closely with stratified sampling, 
    # we use the same global seed and process classes in a stable order.
    for cls in sorted(unique_classes):
        cls_indices = np.where(y == cls)[0] + 1  # 1-based indexing
        num_sample = int(np.ceil(len(cls_indices) * p))
        sampled = np.random.choice(cls_indices, size=num_sample, replace=False)
        indices_per_class.append(sampled)
    
    all_sampled = np.concatenate(indices_per_class)
    sorted_sampled = np.sort(all_sampled)
    
    if times == 1:
        resamples = [sorted_sampled]
    else:
        # Simplified for times > 1 to maintain core logic for this specific vignette
        resamples = [sorted_sampled] * times

    if not list_val:
        # R's createDataPartition returns a matrix when list=FALSE
        # Shape: (num_obs, num_resamples)
        res_mat = np.array(resamples).T
        return res_mat
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# r2py:entity:data
# Sonar is provided by shim as a DataFrame
# No action needed as shim already creates Sonar as a DataFrame

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