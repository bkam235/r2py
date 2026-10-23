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
    if isinstance(obj, np.ndarray):
        rows, cols = obj.shape
        vals = obj[:10, 0]
        val_str = " ".join(map(str, vals))
        print(f"  int [1:{rows}, {cols}] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print("  ..$ : chr \"Resample1\"")
    elif isinstance(obj, pd.DataFrame):
        rows, cols = obj.shape
        vals = obj.iloc[:10, 0].values
        val_str = " ".join(map(str, vals))
        print(f"  int [1:{rows}, {cols}] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print(f"  ..$ : chr \"{obj.columns[0]}\"")
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, p=0.75, list_val=True, times=1):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # Identify unique classes
    unique_classes = y.unique()
    
    resamples = []
    for t in range(times):
        resample_indices = []
        for cls in unique_classes:
            # Get indices of current class (1-indexed)
            cls_indices = np.where(y == cls)[0] + 1
            
            # Calculate number to sample for this class
            num = int(np.ceil(len(cls_indices) * p))
            
            # Sample indices without replacement
            sampled = np.random.choice(cls_indices, size=num, replace=False)
            resample_indices.extend(sampled)
        
        # caret::createDataPartition sorts the resulting indices
        resamples.append(np.sort(resample_indices))

    if not list_val:
        # Return as a NumPy array (matrix equivalent) to match R's matrix output
        return np.array(resamples).T
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# Sonar is loaded by shim
# r2py:entity:data
# (Sonar already present in globals from shim)

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