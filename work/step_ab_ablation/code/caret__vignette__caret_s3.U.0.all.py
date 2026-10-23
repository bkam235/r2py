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
        # The verification shows R produces a string like "int [1:157, 1] 1 2 3 4 5 7 10 11 12 13 ..."
        # We extract the first column's values to match the output format
        vals = obj.iloc[:, 0].values
        val_str = " ".join(map(str, vals[:10]))
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
    
    # Stratified sampling
    indices = np.arange(1, n + 1)
    df = pd.DataFrame({'y': y, 'index': indices})
    
    resamples = []
    for j in range(times):
        resample_indices = []
        # Caret groups by the target levels
        for name, group in df.groupby('y'):
            # R's createDataPartition uses ceiling(nrow(group) * p)
            num = int(np.ceil(len(group) * p))
            # Sample without replacement
            sampled = np.random.choice(group['index'].values, size=num, replace=False)
            resample_indices.extend(sampled)
        
        # R sorts the indices of the resample
        resamples.append(np.sort(resample_indices))

    if not list_val:
        # Return as a matrix (DataFrame in Python)
        res_mat = np.array(resamples).T
        df_out = pd.DataFrame(res_mat, columns=[f"Resample{i+1}" for i in range(times)])
        # Cast to int to avoid float representation in DataFrame
        return df_out.astype(int)
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# Sonar is loaded by shim
# r2py:entity:data
# (Sonar already exists in global scope)

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