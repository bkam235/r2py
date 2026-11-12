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
    # R output for a matrix/dataframe of indices
    # int [1:157, 1] 1 2 3 4 5 7 10 11 12 13 ...
    # - attr(*, "dimnames")=List of 2
    #  ..$ : NULL
    #  ..$ : chr "Resample1"
    if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], list):
        rows = len(obj)
        cols = len(obj[0])
        # Flatten first column for the string representation
        vals = [obj[i][0] for i in range(min(10, rows))]
        val_str = " ".join(map(str, vals))
        print(f"  int [1:{rows}, {cols}] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print("  ..$ : chr \"Resample1\"")
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, p=0.75, list_val=True):
    """
    Python implementation approximating caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # In R's caret, createDataPartition for factors performs stratified sampling.
    # We group by the class and sample p fraction from each group.
    indices = np.arange(1, n + 1)
    df = pd.DataFrame({'y': y, 'index': indices})
    
    resample_indices = []
    for name, group in df.groupby('y'):
        # ceiling(nrow(group) * p)
        num = int(np.ceil(len(group) * p))
        # Sample indices without replacement
        sampled = np.random.choice(group['index'].values, size=num, replace=False)
        resample_indices.extend(sampled)
    
    # Sort indices as caret does
    resample_indices = np.sort(resample_indices)

    if not list_val:
        # Return as a list of lists (each element is [index]) to mimic 
        # R's matrix representation in the verification output [[1], [2], ...]
        return [[int(i)] for i in resample_indices]
    else:
        return {"Resample1": resample_indices}

# Sonar is already loaded by the data shim as a DataFrame
# r2py:entity:data
# No action needed, Sonar is already in globals

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