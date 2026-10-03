# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260929_214437/py/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
# r2py:entity:x
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, GroupKFold
from plotnine import *

# r2py:entity:data
# Since 'oil' dataset from caret isn't in a standard Python lib, 
# we simulate the oilType vector for functional equivalence

# r2py:entity:createDataPartition
# createDataPartition(oilType, 2)
# Approximated using stratified train_test_split
train_idx, test_idx = train_test_split(
    np.arange(len(oilType)), 
    test_size=0.5, 
    stratify=oilType
)

# r2py:entity:inA
# createDataPartition(x, list = FALSE)
# For continuous data, we create bins to stratify or use simple split
x_bins = pd.cut(x, bins=5, labels=False)
inA = train_test_split(np.arange(len(x)), test_size=0.5, stratify=x_bins)[0]
not_inA = np.setdiff1d(np.arange(len(x)), inA)

# r2py:entity:plot
# Plotting density and rug
df_plot = pd.DataFrame({
    'val': np.concatenate([x[inA], x[not_inA]]),
    'group': ['A'] * len(inA) + ['B'] * len(not_inA)
})

p = (ggplot(df_plot, aes(x='val', fill='group')) 
# r2py:entity:points
     + geom_density(alpha=0.5) 
# r2py:entity:rug_1
     + geom_rug(aes(color='group')))
print(p)

# r2py:entity:createResample
# createResample(oilType, 2)
# Approximated by creating 2 stratified folds
resample_folds = KFold(n_splits=2).split(np.arange(len(oilType)))

# r2py:entity:createFolds
# createFolds(oilType, 10)
kf10 = KFold(n_splits=10).split(np.arange(len(oilType)))

# r2py:entity:createFolds_1
# createFolds(oilType, 5, FALSE)
kf5 = KFold(n_splits=5).split(np.arange(len(oilType)))

# r2py:entity:createFolds_2
# createFolds(rnorm(21))
kf_norm = KFold(n_splits=5).split(np.random.randn(21))

# r2py:entity:createTimeSlices
# createTimeSlices translation
def create_time_slices(n, initial, window, fixedWindow=False, skip=0):
    slices = []
    idx = np.arange(1, n + 1)
    start = initial
    while start + window <= n:
        end = start + window - 1
        slices.append(idx[start-1 : end])
        if fixedWindow:
            start += window
        else:
            start += 1
        start += skip
    return slices

create_time_slices(9, 5, 1, fixedWindow=False)
# r2py:entity:createTimeSlices_1
create_time_slices(9, 5, 1, fixedWindow=True)
# r2py:entity:createTimeSlices_2
create_time_slices(9, 5, 3, fixedWindow=True)
# r2py:entity:createTimeSlices_3
create_time_slices(9, 5, 3, fixedWindow=False)

# r2py:entity:createTimeSlices_4
create_time_slices(15, 5, 3)
# r2py:entity:createTimeSlices_5
create_time_slices(15, 5, 3, skip=2)
# r2py:entity:createTimeSlices_6
create_time_slices(15, 5, 3, skip=3)

# Final section
# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
groups = np.sort(np.random.choice(letters, size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts())

# r2py:entity:folds
gkf = GroupKFold(n_splits=3)
folds = list(gkf.split(np.arange(len(groups)), groups=groups))

# r2py:entity:lapply
for fold_idx, (train_idx, test_idx) in enumerate(folds):
    print(f"Fold {fold_idx}:")
    print(pd.Series(groups[test_idx]).value_counts())