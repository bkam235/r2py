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
        if isinstance(obj, pd.DataFrame):
            data = obj.values
            cols = obj.columns
        else:
            data = obj
            cols = [None] * data.shape[1]
            
        rows, cols_count = data.shape
        # R's str output for integer vectors/matrices
        vals = data.flatten()[:10]
        val_str = " ".join(map(str, vals.astype(int)))
        print(f"  int [{1}:{rows}, {cols_count}] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        # If it's a dataframe, the second dimname is the column name
        col_name = cols[0] if (cols and cols[0] is not None) else "Resample1"
        print(f"  ..$ : chr \"{col_name}\"")
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, p=0.75, list_val=False, times=1):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # R's createDataPartition samples within each class
    unique_classes = y.unique()
    all_indices = []
    
    # We use a temporary random state to avoid interfering with global seed
    # but since the original uses set.seed(), we use np.random directly
    for cls in unique_classes:
        cls_indices = np.where(y == cls)[0] + 1 # 1-based indexing
        n_cls = len(cls_indices)
        num_sample = int(np.ceil(n_cls * p))
        
        # To better match R's sample(), we shuffle then take slice
        # Note: np.random.choice without replacement is similar to sample()
        sampled = np.random.choice(cls_indices, size=num_sample, replace=False)
        all_indices.extend(sampled)
    
    # R sorts the resulting indices for a single resample
    sorted_indices = np.sort(all_indices)
    
    if not list_val:
        # Return as a 2D numpy array (column vector) to match R's matrix return
        return sorted_indices.reshape(-1, 1)
    else:
        return {"Resample1": sorted_indices}

# Sonar is provided by shim as a DataFrame
# r2py:entity:data
# (Sonar is already in globals via shim)

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