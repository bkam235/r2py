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
    """Equivalent to R's str() for indices."""
    if isinstance(obj, (pd.DataFrame, pd.Series, np.ndarray)):
        # Mimic R's str output for an integer vector
        # e.g., int [1:156] 1 2 4 5 ...
        flat_obj = np.array(obj).flatten()
        rows = len(flat_obj)
        vals = flat_obj[:10]
        val_str = " ".join(map(str, vals))
        print(f" int [1:{rows}] {val_str} ...")
    else:
        print(repr(obj))

# r2py:entity:inTrain
def create_data_partition(y, p=0.5, list_val=True, times=1, groups=None):
    """
    Python implementation of caret's createDataPartition.
    """
    y = pd.Series(y)
    n = len(y)
    
    if np.issubdtype(y.dtype, np.number):
        # Approximate R's binning for numeric
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
        # Group by target to perform stratified sampling
        for name, group in df.groupby('y'):
            num = int(np.ceil(len(group) * p))
            sampled = np.random.choice(group['index'].values, size=num, replace=False)
            resample_indices.extend(sampled)
        
        resamples.append(np.sort(resample_indices))

    if not list_val:
        # If times=1 and list=FALSE, R returns a simple integer vector
        if times == 1:
            return resamples[0]
        else:
            # Return as matrix-like (indices as columns)
            res_mat = np.array(resamples).T
            df_out = pd.DataFrame(res_mat)
            df_out.columns = [f"Resample{i+1}" for i in range(times)]
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