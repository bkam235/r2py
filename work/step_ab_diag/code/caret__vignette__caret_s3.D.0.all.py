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
        # R's str(inTrain) for list=FALSE returns a matrix
        # Output: int [1:157, 1] 1 2 3 4 5 7 10 11 12 13 ...
        # - attr(*, "dimnames")=List of 2
        # ..$ : NULL
        # ..$ : chr "Resample1"
        
        if isinstance(obj, pd.DataFrame):
            data = obj.values
            cols = obj.columns
        else:
            data = obj
            cols = ["Resample1"] # Default name if it's just a numpy array
            
        rows, cols_count = data.shape
        # Take the first 10 elements of the first column
        vals = data[:10, 0]
        val_str = " ".join(map(str, vals.astype(int)))
        
        print(f"  int [1:{rows}, {cols_count}] {val_str} ...")
        print(' - attr(*, "dimnames")=List of 2')
        print('  ..$ : NULL')
        col_name = cols[0] if len(cols) > 0 else "Resample1"
        print(f'  ..$ : chr "{col_name}"')
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, p=0.5, list_val=True, times=1):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # caret's createDataPartition performs stratified sampling
    # based on the levels of the factor y.
    unique_levels = y.unique()
    
    resamples = []
    for t in range(times):
        all_indices = []
        for level in unique_levels:
            # Get indices where y == level (1-indexed for R parity)
            level_indices = np.where(y == level)[0] + 1
            
            # Calculate number of samples for this level: ceil(len * p)
            num_samples = int(np.ceil(len(level_indices) * p))
            
            # Sample without replacement
            sampled = np.random.choice(level_indices, size=num_samples, replace=False)
            all_indices.extend(sampled)
        
        # caret sorts the result of the partition
        resamples.append(np.sort(all_indices))

    if not list_val:
        # Returns a matrix in R
        res_mat = np.array(resamples).T
        df_out = pd.DataFrame(res_mat, columns=[f"Resample{i+1}" for i in range(times)])
        return df_out
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# Sonar is provided by shim as a DataFrame
# r2py:entity:data
# (Sonar is already loaded via shim)

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