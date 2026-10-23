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
            cols = None
        
        rows, cols_count = data.shape
        # R's str for matrix: int [1:157, 1] 1 2 3 ...
        # Use a small number of samples for the string
        vals = data[:10, 0]
        val_str = " ".join(map(str, vals))
        
        # Column name for "Resample1"
        col_name = "Resample1" if cols is None or (hasattr(cols, '__getitem__') and len(cols) > 0) else "V1"
        if cols is not None and hasattr(cols, '__getitem__') and len(cols) > 0:
            col_name = cols[0]

        print(f"  int [1:{rows}, {cols_count}] {val_str} ...")
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
    
    # Handle numeric y by binning
    if np.issubdtype(y.dtype, np.number):
        if groups is None:
            groups = min(5, n)
        bins = np.unique(np.quantile(y, np.linspace(0, 1, groups + 1)))
        y_fact = pd.cut(y, bins=bins, include_lowest=True)
    else:
        y_fact = y

    indices = np.arange(1, n + 1)
    df = pd.DataFrame({'y': y_fact, 'index': indices})
    
    resamples = []
    for j in range(times):
        resample_indices = []
        # Stratified sampling: for each class, sample p%
        for name, group in df.groupby('y'):
            num = int(np.ceil(len(group) * p))
            # Randomly sample without replacement
            sampled = np.random.choice(group['index'].values, size=num, replace=False)
            resample_indices.extend(sampled)
        
        # caret sorts the resulting index vector
        resamples.append(np.sort(resample_indices))

    if not list_val:
        # Return as a numpy array (mimics the R matrix)
        # shape (n_samples, times)
        res_mat = np.array(resamples).T
        return res_mat
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

# Sonar is provided by shim as a DataFrame
# r2py:entity:data
# (Sonar is already defined by the shim)

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