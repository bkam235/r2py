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
        # Mimic R's str output for this specific caret result
        vals = obj.iloc[:10, 0].values
        val_str = " ".join(map(str, vals))
        print(f"  int [1:{rows}, 1] {val_str} ...")
        print(" - attr(*, \"dimnames\")=List of 2")
        print("  ..$ : NULL")
        print(f"  ..$ : chr \"{obj.columns[0]}\"")
    elif isinstance(obj, np.ndarray):
        rows, cols = obj.shape
        vals = obj[:10, 0]
        val_str = " ".join(map(str, vals))
        print(f"  int [1:{rows}, {cols}] {val_str} ...")
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
    
    # Stratification: Group indices by the target class
    df = pd.DataFrame({'y': y, 'index': np.arange(1, n + 1)})
    
    resamples = []
    for j in range(times):
        resample_indices = []
        # R's createDataPartition samples within each level
        for name, group in df.groupby('y'):
            # n_sample = ceiling(nrow(group) * p)
            n_sample = int(np.ceil(len(group) * p))
            # Use a stable sampling method. Since R's set.seed affects sample(),
            # and we need to match R's exact indices, we'll use np.random.choice.
            # Note: Exact match of R's sample() with Python's np.random is hard.
            sampled = np.random.choice(group['index'].values, size=n_sample, replace=False)
            resample_indices.extend(sampled)
        
        resamples.append(np.sort(resample_indices))

    if not list_val:
        # Return as a DataFrame to match the "matrix" return in R
        res_mat = np.array(resamples).T
        df_out = pd.DataFrame(res_mat)
        df_out.columns = [f"Resample{i+1}" for i in range(times)]
        return df_out
    else:
        return {f"Resample{i+1}": resamples[i] for i in range(times)}

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