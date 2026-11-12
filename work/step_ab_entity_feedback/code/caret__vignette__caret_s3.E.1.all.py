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
        # R's str(inTrain) for the result of createDataPartition(list=FALSE) 
        # looks like: int [1:157, 1] 1 2 3 4 5 7 10 11 12 13 ...
        # - attr(*, "dimnames")=List of 2
        # ..$ : NULL
        # ..$ : chr "Resample1"
        if isinstance(obj, pd.DataFrame):
            data_arr = obj.values
            cols = obj.columns
        else:
            data_arr = obj
            cols = ["Resample1"] # Default for createDataPartition
            
        rows, cols_count = data_arr.shape
        # Take first 10 elements of the first column
        vals = data_arr[:10, 0]
        val_str = " ".join(map(str, vals.astype(int)))
        print(f"  int [1:{rows}, 1] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print(f"  ..$ : chr \"{cols[0] if isinstance(cols, (list, pd.Index)) else 'Resample1'}\"")
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, p=0.5, list_val=True, times=1):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # Indices 1 to N (R style)
    indices = np.arange(1, n + 1)
    df = pd.DataFrame({'y': y, 'index': indices})
    
    resamples = []
    for _ in range(times):
        resample_indices = []
        # Group by the target to perform stratified sampling
        for name, group in df.groupby('y'):
            # R's ceiling(nrow(dat) * p)
            num = int(np.ceil(len(group) * p))
            # Sample indices without replacement
            # We use np.random.permutation to get a shuffle and then slice, 
            # which is often closer to R's sample() behavior than np.random.choice
            perm = np.random.permutation(group['index'].values)
            sampled = perm[:num]
            resample_indices.extend(sampled)
        
        # R's createDataPartition sorts the resulting indices
        resamples.append(np.sort(resample_indices))

    if not list_val:
        # Return as a 2D numpy array (mimics the matrix return in R)
        # shape: (n_samples, times)
        res_mat = np.array(resamples).T
        return res_mat
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# Sonar is provided by shim as a DataFrame
# r2py:entity:data
# (Handled by shim)

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