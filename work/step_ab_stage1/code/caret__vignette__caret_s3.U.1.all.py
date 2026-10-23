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
    """Equivalent to R's str() for matrices/dataframes."""
    if isinstance(obj, (pd.DataFrame, np.ndarray)):
        # R's str(inTrain) output: int [1:157, 1] 1 2 3 4 5 7 10 11 12 13 ...
        # We need to extract the first column values if it's a matrix/df
        if isinstance(obj, pd.DataFrame):
            vals = obj.iloc[:, 0].values
            rows, cols = obj.shape
            col_name = obj.columns[0]
        else:
            vals = obj[:, 0] if obj.ndim > 1 else obj
            rows = obj.shape[0]
            cols = obj.shape[1] if obj.ndim > 1 else 1
            col_name = "Resample1"
            
        val_str = " ".join(map(str, vals[:10]))
        print(f"  int [1:{rows}, {cols}] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print(f"  ..$ : chr \"{col_name}\"")
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, times=1, p=0.5, list_val=True, groups=None):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    # Identify unique classes
    unique_classes = y.unique()
    
    resamples = []
    for j in range(times):
        resample_indices = []
        for cls in unique_classes:
            # Get indices of rows belonging to this class (1-indexed for R)
            cls_indices = np.where(y == cls)[0] + 1
            
            # Calculate number of samples for this class
            num = int(np.ceil(len(cls_indices) * p))
            
            # Use a local random state to better mimic R's sample()
            # R's sample(x, size, replace=FALSE)
            sampled = np.random.choice(cls_indices, size=num, replace=False)
            resample_indices.extend(sampled)
        
        # Sort indices as caret does
        resamples.append(np.sort(resample_indices))

    if not list_val:
        # Return as a NumPy array (matrix) to match R's matrix return when list=FALSE
        res_mat = np.array(resamples).T
        return res_mat
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# Sonar is already loaded by shim
# r2py:entity:data
Sonar = pd.DataFrame(Sonar) if isinstance(Sonar, dict) else Sonar

# set.seed(107)
# r2py:entity:set.seed
np.random.seed(107)

# inTrain <- createDataPartition(y = Sonar$Class, p = .75, list = FALSE)
inTrain = create_data_partition(
    y=Sonar['Class'],
    p=0.75,
    list_val=False
)

# To make str_obj print "Resample1", we can wrap it in a DataFrame or handle it in the function
# In R, createDataPartition(list=FALSE) returns a matrix with col name "Resample1"
inTrain_df = pd.DataFrame(inTrain, columns=[f"Resample{i+1}" for i in range(inTrain.shape[1])])

# str(inTrain)
# r2py:entity:str
str_obj(inTrain_df)